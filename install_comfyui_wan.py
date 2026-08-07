#!/usr/bin/env python3
"""
ComfyUI + Wan2.1 local installer  (Windows / Linux, NVIDIA GPU)

Free and local only: official GitHub repos + official Hugging Face weights.
No paid APIs, no cloud services, no modified binaries.

Usage
-----
    python install_comfyui_wan.py                 # inspect hardware only, change nothing
    python install_comfyui_wan.py --install       # inspect, ask, then install
    python install_comfyui_wan.py --install --dir D:\\AI\\ComfyUI

Stdlib only, so it runs before anything is set up.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# --------------------------------------------------------------------------
# Sources. Official repositories and the Comfy-Org repackaged weights only.
# --------------------------------------------------------------------------

COMFYUI_REPO = "https://github.com/comfyanonymous/ComfyUI.git"
MANAGER_REPO = "https://github.com/Comfy-Org/ComfyUI-Manager.git"

HF_BASE = (
    "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged"
    "/resolve/main/split_files"
)

# name -> (url suffix, destination folder under models/, bytes)
# Sizes are the real published sizes, used for the disk-space check and to
# detect truncated downloads.
FILES = {
    "t2v_1.3B": (
        "diffusion_models/wan2.1_t2v_1.3B_fp16.safetensors",
        "diffusion_models",
        2_838_303_560,
    ),
    "text_encoder": (
        "text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors",
        "text_encoders",
        6_735_906_897,
    ),
    "vae": (
        "vae/wan_2.1_vae.safetensors",
        "vae",
        253_815_318,
    ),
    "clip_vision": (
        "clip_vision/clip_vision_h.safetensors",
        "clip_vision",
        1_264_219_396,
    ),
    "i2v_480p_14B": (
        "diffusion_models/wan2.1_i2v_480p_14B_fp8_scaled.safetensors",
        "diffusion_models",
        16_401_356_938,
    ),
}

GB = 1024 ** 3


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

class Abort(Exception):
    """Raised for any condition that should stop the install cleanly."""


def say(msg: str = "") -> None:
    print(msg, flush=True)


def head(title: str) -> None:
    say("\n" + "=" * 68)
    say(f"  {title}")
    say("=" * 68)


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    """Run a command, streaming output. Raises Abort with a readable message."""
    say(f"  $ {' '.join(str(c) for c in cmd)}")
    try:
        return subprocess.run(cmd, check=True, **kw)
    except FileNotFoundError:
        raise Abort(f"Command not found: {cmd[0]}")
    except subprocess.CalledProcessError as exc:
        raise Abort(f"Command failed (exit {exc.returncode}): {' '.join(cmd)}")


def probe(cmd: list[str]) -> str | None:
    """Run a command and return stdout, or None if it isn't available."""
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def human(n: float) -> str:
    return f"{n / GB:.1f} GB"


# --------------------------------------------------------------------------
# 1. Hardware inspection
# --------------------------------------------------------------------------

def inspect() -> dict:
    """Gather everything needed for the compatibility decision."""
    info: dict = {
        "os": platform.system(),
        "os_detail": platform.platform(),
        "python": sys.version.split()[0],
        "python_ok": sys.version_info >= (3, 10),
        "cores": os.cpu_count() or 1,
        "git": shutil.which("git") is not None,
        "ffmpeg": shutil.which("ffmpeg") is not None,
        "gpu": None,
        "vram_gb": 0.0,
        "driver": None,
        "cuda": None,
        "ram_gb": 0.0,
        "disk_gb": 0.0,
    }

    # RAM
    try:
        if info["os"] == "Windows":
            import ctypes

            class MEMSTAT(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            st = MEMSTAT()
            st.dwLength = ctypes.sizeof(MEMSTAT)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(st))
            info["ram_gb"] = st.ullTotalPhys / GB
        else:
            info["ram_gb"] = (
                os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / GB
            )
    except Exception:
        pass

    # GPU via nvidia-smi. This is the authoritative source for both VRAM and
    # the maximum CUDA version the installed driver supports.
    smi = probe([
        "nvidia-smi",
        "--query-gpu=name,memory.total,driver_version",
        "--format=csv,noheader",
    ])
    if smi:
        first = smi.splitlines()[0]
        parts = [p.strip() for p in first.split(",")]
        if len(parts) >= 3:
            info["gpu"] = parts[0]
            m = re.search(r"(\d+)", parts[1])
            if m:
                info["vram_gb"] = int(m.group(1)) / 1024
            info["driver"] = parts[2]

        banner = probe(["nvidia-smi"]) or ""
        m = re.search(r"CUDA Version:\s*([\d.]+)", banner)
        if m:
            info["cuda"] = m.group(1)

    return info


def report(info: dict) -> None:
    head("1. SYSTEM INSPECTION")
    say(f"  Operating system : {info['os_detail']}")
    say(f"  Python           : {info['python']}"
        f"{'' if info['python_ok'] else '   <-- 3.10+ required'}")
    say(f"  CPU cores        : {info['cores']}")
    say(f"  System RAM       : {info['ram_gb']:.1f} GB")
    say(f"  Free disk        : {info['disk_gb']:.1f} GB  (at install target)")
    say("")
    if info["gpu"]:
        say(f"  GPU              : {info['gpu']}")
        say(f"  VRAM             : {info['vram_gb']:.1f} GB")
        say(f"  Driver           : {info['driver']}")
        say(f"  CUDA (max)       : {info['cuda']}")
    else:
        say("  GPU              : none detected (nvidia-smi unavailable)")
    say("")
    say(f"  git              : {'found' if info['git'] else 'MISSING'}")
    say(f"  ffmpeg           : {'found' if info['ffmpeg'] else 'MISSING'}")


# --------------------------------------------------------------------------
# 2. Compatibility gate — nothing is installed before this passes
# --------------------------------------------------------------------------

def plan(info: dict) -> dict:
    """Decide what to install. Raises Abort if the machine can't run this."""
    head("2. COMPATIBILITY CHECK")

    if info["os"] not in ("Windows", "Linux"):
        raise Abort(
            f"{info['os']} is not supported by this installer.\n"
            "  Wan2.1 in ComfyUI needs an NVIDIA CUDA GPU. Apple Silicon can run\n"
            "  ComfyUI via MPS but Wan video generation is impractically slow there."
        )

    if not info["python_ok"]:
        raise Abort(
            f"Python {info['python']} is too old. ComfyUI needs 3.10 or newer.\n"
            "  Install Python 3.12 from https://www.python.org/downloads/ and re-run.\n"
            "  This script will not modify your system Python."
        )

    if not info["gpu"]:
        raise Abort(
            "No NVIDIA GPU detected.\n"
            "  'nvidia-smi' did not return a GPU, so there is no CUDA device to\n"
            "  target. Wan2.1 needs an NVIDIA card; CPU-only generation would take\n"
            "  many hours per clip.\n"
            "  If you do have an NVIDIA GPU, install/repair the driver from\n"
            "  https://www.nvidia.com/Download/index.aspx and re-run this check."
        )

    vram = info["vram_gb"]
    if vram < 5.5:
        raise Abort(
            f"Only {vram:.1f} GB VRAM detected. Wan2.1 T2V-1.3B needs roughly 6 GB\n"
            "  even with aggressive offloading. This GPU is below the practical floor."
        )

    # Model tier from VRAM (requirements 10 and 11).
    want = ["t2v_1.3B", "text_encoder", "vae"]
    if vram >= 12:
        want += ["clip_vision", "i2v_480p_14B"]
        i2v = "wan2.1_i2v_480p_14B_fp8_scaled.safetensors"
        i2v_note = (
            "comfortable" if vram >= 16 else "works, but will offload and run slowly"
        )
    else:
        i2v = None
        i2v_note = (
            f"skipped — the 14B I2V model needs 12 GB+ VRAM, you have {vram:.1f} GB"
        )

    # VRAM flags (requirement 15).
    if vram < 8:
        flag = "--lowvram"
    elif vram < 12:
        flag = "--normalvram"
    else:
        flag = ""

    # CUDA wheel index from the driver's max CUDA version.
    cuda = info["cuda"] or "0"
    try:
        major, minor = (int(x) for x in cuda.split(".")[:2])
    except ValueError:
        major, minor = 0, 0
    # major*100+minor so 12.10 doesn't collide with 13.0.
    ver = major * 100 + minor
    if ver >= 1208:
        # Blackwell (50-series) requires cu128; also correct for CUDA 13.x.
        wheel, wname = "cu128", "CUDA 12.8+"
    elif ver >= 1200:
        # CUDA 12.x has minor-version compatibility, so any 12.x driver
        # runs cu126 wheels. Preferred over cu118 on modern cards.
        wheel, wname = "cu126", "CUDA 12.x"
    elif ver >= 1108:
        wheel, wname = "cu118", "CUDA 11.8"
    else:
        raise Abort(
            f"Driver reports CUDA {cuda}, which is older than PyTorch's minimum "
            "(11.8).\n  Update your NVIDIA driver and re-run."
        )

    need_bytes = sum(FILES[k][2] for k in want)
    need_gb = need_bytes / GB + 12  # + ComfyUI, venv and PyTorch
    if info["disk_gb"] < need_gb:
        raise Abort(
            f"Not enough disk space. Need about {need_gb:.0f} GB, "
            f"found {info['disk_gb']:.1f} GB free.\n"
            "  Free some space or pass --dir pointing at a larger drive."
        )

    p = {
        "want": want,
        "wheel": wheel,
        "flag": flag,
        "i2v": i2v,
        "need_gb": need_gb,
        "vram": vram,
    }

    say(f"  GPU accepted     : {info['gpu']} ({vram:.1f} GB VRAM)")
    say(f"  PyTorch build    : {wheel}  (matches driver {wname})")
    say(f"  Text-to-video    : wan2.1_t2v_1.3B_fp16.safetensors")
    say(f"  Image-to-video   : {i2v or 'not installed'}")
    say(f"                     {i2v_note}")
    say(f"  VRAM flag        : {flag or '(none needed)'}")
    say(f"  Download size    : {human(need_bytes)}")
    say(f"  Total disk needed: ~{need_gb:.0f} GB")
    return p


def confirm(target: Path) -> None:
    head("CONFIRM BEFORE INSTALLING")
    say(f"  Everything will be installed under:\n    {target}")
    say("")
    say("  This will NOT touch your system Python, PATH, drivers or registry.")
    say("  If git or ffmpeg are missing you will be asked separately.")
    say("")
    if input("  Type 'yes' to continue: ").strip().lower() != "yes":
        raise Abort("Cancelled at your request. Nothing was installed.")


# --------------------------------------------------------------------------
# 3. Prerequisites — only what is missing, and only after asking
# --------------------------------------------------------------------------

def ensure_prereqs(info: dict) -> None:
    head("3. PREREQUISITES")

    if info["git"] and info["ffmpeg"]:
        say("  git and ffmpeg are already present. Nothing to install.")
        return

    missing = [n for n, ok in (("git", info["git"]), ("ffmpeg", info["ffmpeg"])) if not ok]
    say(f"  Missing: {', '.join(missing)}")

    if info["os"] == "Linux":
        say("  These can be installed with apt, which needs sudo.")
        if input("  Run 'sudo apt install' now? [y/N]: ").strip().lower() != "y":
            raise Abort(
                f"Install {' and '.join(missing)} manually, then re-run:\n"
                f"    sudo apt update && sudo apt install -y {' '.join(missing)}"
            )
        run(["sudo", "apt-get", "update"])
        run(["sudo", "apt-get", "install", "-y", *missing])
    else:
        say("\n  On Windows, install these yourself so nothing touches your PATH")
        say("  without your knowledge:")
        if "git" in missing:
            say("    git    ->  winget install --id Git.Git -e")
        if "ffmpeg" in missing:
            say("    ffmpeg ->  winget install --id Gyan.FFmpeg -e")
        raise Abort("Install the tools above, open a new terminal, then re-run.")


# --------------------------------------------------------------------------
# 4-8. ComfyUI, venv, PyTorch, dependencies, Manager
# --------------------------------------------------------------------------

def venv_python(root: Path) -> Path:
    if platform.system() == "Windows":
        return root / "venv" / "Scripts" / "python.exe"
    return root / "venv" / "bin" / "python"


def install_comfy(root: Path, p: dict) -> Path:
    head("4. COMFYUI")
    if (root / ".git").exists():
        say("  Already cloned — pulling latest.")
        run(["git", "-C", str(root), "pull", "--ff-only"])
    else:
        root.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--depth", "1", COMFYUI_REPO, str(root)])

    head("5. VIRTUAL ENVIRONMENT")
    py = venv_python(root)
    if py.exists():
        say("  venv already exists — reusing it.")
    else:
        run([sys.executable, "-m", "venv", str(root / "venv")])
    run([str(py), "-m", "pip", "install", "--upgrade", "pip", "wheel"])

    head("6. PYTORCH (CUDA)")
    say(f"  Installing the {p['wheel']} build. This is a large download.")
    run([
        str(py), "-m", "pip", "install",
        "torch", "torchvision", "torchaudio",
        "--index-url", f"https://download.pytorch.org/whl/{p['wheel']}",
    ])

    # Verify CUDA actually works before going further — a silent CPU-only
    # PyTorch is the most common cause of "it installed but nothing generates".
    check = subprocess.run(
        [str(py), "-c",
         "import torch;print(torch.cuda.is_available());"
         "print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else '')"],
        capture_output=True, text=True,
    )
    if "True" not in check.stdout:
        raise Abort(
            "PyTorch installed but cannot see your GPU.\n"
            f"  torch.cuda.is_available() returned False.\n"
            f"  Output: {check.stdout.strip()} {check.stderr.strip()}\n"
            "  Usually this means the NVIDIA driver is older than the CUDA build.\n"
            "  Update the driver, or re-run and pick a lower cu### build."
        )
    say(f"  CUDA verified: {check.stdout.strip().splitlines()[-1]}")

    head("7. COMFYUI DEPENDENCIES")
    run([str(py), "-m", "pip", "install", "-r", str(root / "requirements.txt")])

    head("8. COMFYUI-MANAGER")
    mgr = root / "custom_nodes" / "ComfyUI-Manager"
    if mgr.exists():
        say("  Already installed.")
    else:
        mgr.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--depth", "1", MANAGER_REPO, str(mgr)])
        req = mgr / "requirements.txt"
        if req.exists():
            run([str(py), "-m", "pip", "install", "-r", str(req)])
    return py


# --------------------------------------------------------------------------
# 9-13. Models
# --------------------------------------------------------------------------

def download(url: str, dest: Path, expect: int) -> None:
    """Resumable download with a progress line. Skips files already complete."""
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists() and dest.stat().st_size == expect:
        say(f"  [ok]  {dest.name} already complete")
        return

    have = dest.stat().st_size if dest.exists() else 0
    if have > expect:
        raise Abort(
            f"{dest} is larger than expected ({have} vs {expect} bytes).\n"
            "  Delete it and re-run — I will not overwrite it without your say-so."
        )

    mode = "ab" if have else "wb"
    req = urllib.request.Request(url, headers={"User-Agent": "comfyui-wan-installer"})
    if have:
        req.add_header("Range", f"bytes={have}-")
        say(f"  [..] {dest.name}: resuming at {human(have)}")
    else:
        say(f"  [..] {dest.name}: {human(expect)}")

    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, mode) as f:
            done = have
            while chunk := r.read(1 << 20):
                f.write(chunk)
                done += len(chunk)
                pct = done / expect * 100
                rate = (done - have) / max(time.time() - start, 0.1) / 1e6
                print(f"\r       {pct:5.1f}%  {human(done)} / {human(expect)}"
                      f"  {rate:5.1f} MB/s", end="", flush=True)
        print()
    except urllib.error.HTTPError as exc:
        raise Abort(f"Download failed for {dest.name}: HTTP {exc.code} — {exc.reason}")
    except urllib.error.URLError as exc:
        raise Abort(f"Download failed for {dest.name}: {exc.reason}\n"
                    "  Check your connection and re-run; downloads resume.")

    got = dest.stat().st_size
    if got != expect:
        raise Abort(
            f"{dest.name} finished at {got} bytes, expected {expect}.\n"
            "  Re-run to resume — the partial file is kept."
        )
    say(f"  [ok]  {dest.name}")


def fetch_models(root: Path, p: dict) -> None:
    head("9-13. MODELS")
    say("  Source: huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged (official)\n")
    for key in p["want"]:
        suffix, folder, size = FILES[key]
        download(f"{HF_BASE}/{suffix}", root / "models" / folder / Path(suffix).name, size)


# --------------------------------------------------------------------------
# 14. Workflows
# --------------------------------------------------------------------------

def t2v_workflow(steps: int = 20, length: int = 33) -> dict:
    """Native Wan2.1 text-to-video, ComfyUI API format."""
    return {
        "1": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
            "type": "wan", "device": "default"}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["1", 0],
            "text": "a golden coin half buried in dark soil, camera slowly pushes in, "
                    "sunlight catches the metal, cinematic, shallow depth of field"}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["1", 0],
            "text": "blurry, low quality, distorted, watermark, text, static"}},
        "4": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "wan2.1_t2v_1.3B_fp16.safetensors",
            "weight_dtype": "default"}},
        "5": {"class_type": "ModelSamplingSD3", "inputs": {
            "model": ["4", 0], "shift": 8.0}},
        "6": {"class_type": "VAELoader", "inputs": {
            "vae_name": "wan_2.1_vae.safetensors"}},
        "7": {"class_type": "EmptyHunyuanLatentVideo", "inputs": {
            "width": 480, "height": 480, "length": length, "batch_size": 1}},
        "8": {"class_type": "KSampler", "inputs": {
            "model": ["5", 0], "positive": ["2", 0], "negative": ["3", 0],
            "latent_image": ["7", 0], "seed": 42, "steps": steps, "cfg": 6.0,
            "sampler_name": "uni_pc", "scheduler": "simple", "denoise": 1.0}},
        "9": {"class_type": "VAEDecode", "inputs": {
            "samples": ["8", 0], "vae": ["6", 0]}},
        "10": {"class_type": "SaveAnimatedWEBP", "inputs": {
            "images": ["9", 0], "filename_prefix": "wan_t2v",
            "fps": 16.0, "lossless": False, "quality": 90, "method": "default"}},
    }


def i2v_workflow() -> dict:
    """Native Wan2.1 image-to-video, ComfyUI API format."""
    return {
        "1": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
            "type": "wan", "device": "default"}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["1", 0],
            "text": "the scene comes alive, gentle natural motion, cinematic"}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["1", 0],
            "text": "blurry, low quality, distorted, watermark, text"}},
        "4": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "wan2.1_i2v_480p_14B_fp8_scaled.safetensors",
            "weight_dtype": "default"}},
        "5": {"class_type": "ModelSamplingSD3", "inputs": {
            "model": ["4", 0], "shift": 8.0}},
        "6": {"class_type": "VAELoader", "inputs": {
            "vae_name": "wan_2.1_vae.safetensors"}},
        "7": {"class_type": "CLIPVisionLoader", "inputs": {
            "clip_name": "clip_vision_h.safetensors"}},
        "8": {"class_type": "LoadImage", "inputs": {
            "image": "example.png", "upload": "image"}},
        "9": {"class_type": "CLIPVisionEncode", "inputs": {
            "clip_vision": ["7", 0], "image": ["8", 0], "crop": "none"}},
        "10": {"class_type": "WanImageToVideo", "inputs": {
            "positive": ["2", 0], "negative": ["3", 0], "vae": ["6", 0],
            "clip_vision_output": ["9", 0], "start_image": ["8", 0],
            "width": 480, "height": 480, "length": 33, "batch_size": 1}},
        "11": {"class_type": "KSampler", "inputs": {
            "model": ["5", 0], "positive": ["10", 0], "negative": ["10", 1],
            "latent_image": ["10", 2], "seed": 42, "steps": 20, "cfg": 6.0,
            "sampler_name": "uni_pc", "scheduler": "simple", "denoise": 1.0}},
        "12": {"class_type": "VAEDecode", "inputs": {
            "samples": ["11", 0], "vae": ["6", 0]}},
        "13": {"class_type": "SaveAnimatedWEBP", "inputs": {
            "images": ["12", 0], "filename_prefix": "wan_i2v",
            "fps": 16.0, "lossless": False, "quality": 90, "method": "default"}},
    }


def write_workflows(root: Path, p: dict) -> Path:
    head("14. WORKFLOWS")
    wf = root / "user" / "default" / "workflows"
    wf.mkdir(parents=True, exist_ok=True)

    (wf / "wan_t2v_api.json").write_text(json.dumps(t2v_workflow(), indent=2))
    say(f"  wrote {wf / 'wan_t2v_api.json'}")

    if p["i2v"]:
        (wf / "wan_i2v_api.json").write_text(json.dumps(i2v_workflow(), indent=2))
        say(f"  wrote {wf / 'wan_i2v_api.json'}")
    else:
        say("  image-to-video workflow skipped (needs 12 GB+ VRAM)")

    say("\n  These are API-format graphs, used by the verification step below.")
    say("  For interactive editing, ComfyUI also ships maintained Wan templates:")
    say("  Workflow menu -> Browse Templates -> Video -> Wan 2.1.")
    return wf


# --------------------------------------------------------------------------
# 15, 20. Launch scripts
# --------------------------------------------------------------------------

def write_launchers(root: Path, p: dict) -> None:
    head("15 + 20. VRAM SETTINGS AND START SCRIPTS")
    flag = p["flag"]
    say(f"  VRAM flag baked into the launcher: {flag or '(none needed)'}")

    if platform.system() == "Windows":
        f = root / "start_comfyui.bat"
        f.write_text(
            "@echo off\r\n"
            f'cd /d "{root}"\r\n'
            f'call "venv\\Scripts\\activate.bat"\r\n'
            f"python main.py {flag}\r\n"
            "pause\r\n"
        )
        say(f"  wrote {f}   (double-click to launch)")
    else:
        f = root / "start_comfyui.sh"
        f.write_text(
            "#!/usr/bin/env bash\n"
            "set -e\n"
            f'cd "{root}"\n'
            'source venv/bin/activate\n'
            f"python main.py {flag}\n"
        )
        f.chmod(0o755)
        say(f"  wrote {f}   (run with ./start_comfyui.sh)")


# --------------------------------------------------------------------------
# 16, 17. Launch and verify
# --------------------------------------------------------------------------

def api(url: str, payload: dict | None = None, timeout: int = 15):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"} if data else {},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def launch_and_verify(root: Path, py: Path, p: dict, wf_dir: Path) -> None:
    head("16. STARTING COMFYUI")
    cmd = [str(py), "main.py"] + ([p["flag"]] if p["flag"] else [])
    say(f"  $ {' '.join(cmd)}")
    proc = subprocess.Popen(
        cmd, cwd=str(root),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    base = "http://127.0.0.1:8188"
    say(f"  Waiting for {base} ...")
    for _ in range(120):
        if proc.poll() is not None:
            raise Abort(
                "ComfyUI exited during startup.\n"
                f"  Run it manually to see the error:  cd {root} && "
                f"{py} main.py {p['flag']}"
            )
        try:
            api(f"{base}/system_stats", timeout=2)
            break
        except Exception:
            time.sleep(1)
    else:
        proc.terminate()
        raise Abort("ComfyUI did not respond within 120s.")

    say(f"\n  ComfyUI is running at:  {base}")
    say("  Open that address in your browser.\n")

    head("17. TEST RENDER")
    # Version drift is the main risk with a hand-written graph, so check every
    # node exists in this build before submitting anything.
    try:
        known = set(api(f"{base}/object_info", timeout=60))
    except Exception as exc:
        say(f"  Could not read /object_info ({exc}); skipping the test render.")
        say("  ComfyUI is still running — try a template from the UI.")
        return

    graph = t2v_workflow(steps=6, length=17)  # deliberately tiny
    unknown = sorted({n["class_type"] for n in graph.values()} - known)
    if unknown:
        say(f"  Skipping: this ComfyUI build has no node(s) {', '.join(unknown)}.")
        say("  Your install is fine — the graph just needs different node names.")
        say("  Use Workflow -> Browse Templates -> Video -> Wan 2.1 instead.")
        return

    say("  Submitting a 17-frame, 6-step 480x480 clip (small on purpose)...")
    try:
        pid = api(f"{base}/prompt", {"prompt": graph})["prompt_id"]
    except Exception as exc:
        say(f"  Could not queue the test job: {exc}")
        return

    for _ in range(900):  # up to 15 minutes
        time.sleep(2)
        try:
            hist = api(f"{base}/history/{pid}", timeout=10)
        except Exception:
            continue
        if pid in hist:
            outs = hist[pid].get("outputs", {})
            files = [i.get("filename") for o in outs.values()
                     for i in o.get("images", []) if i.get("filename")]
            if files:
                say(f"\n  SUCCESS — wrote {', '.join(files)}")
                say(f"  Find it in: {root / 'output'}")
            else:
                say("\n  The job finished but produced no file. Check the ComfyUI log.")
            return
    say("\n  Test still running after 15 minutes — leaving it to finish.")
    say(f"  Watch progress at {base}")


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Install ComfyUI + Wan2.1 locally.")
    ap.add_argument("--install", action="store_true",
                    help="actually install; without this, only inspect")
    ap.add_argument("--dir", default=None, help="install location")
    ap.add_argument("--no-test", action="store_true",
                    help="skip the launch and test render")
    args = ap.parse_args()

    root = Path(args.dir).expanduser().resolve() if args.dir \
        else Path.home() / "ComfyUI"

    try:
        info = inspect()
        probe_dir = root if root.exists() else root.parent
        while not probe_dir.exists() and probe_dir != probe_dir.parent:
            probe_dir = probe_dir.parent
        info["disk_gb"] = shutil.disk_usage(probe_dir).free / GB

        report(info)
        p = plan(info)

        if not args.install:
            head("CHECK ONLY — NOTHING INSTALLED")
            say("  Your system passed every compatibility check.")
            say("  To install, re-run with:")
            say(f"      python {Path(__file__).name} --install"
                + (f" --dir {root}" if args.dir else ""))
            return 0

        confirm(root)
        ensure_prereqs(info)
        py = install_comfy(root, p)
        fetch_models(root, p)
        wf_dir = write_workflows(root, p)
        write_launchers(root, p)

        if args.no_test:
            head("DONE")
            say(f"  Start ComfyUI with the script in {root}")
        else:
            launch_and_verify(root, py, p, wf_dir)

        head("INSTALLED")
        say(f"  Location : {root}")
        say(f"  Launch   : {'start_comfyui.bat' if info['os'] == 'Windows' else './start_comfyui.sh'}")
        say(f"  URL      : http://127.0.0.1:8188")
        return 0

    except Abort as exc:
        say(f"\n[STOPPED] {exc}\n")
        return 1
    except KeyboardInterrupt:
        say("\n[STOPPED] Interrupted. Downloads resume if you re-run.\n")
        return 130


if __name__ == "__main__":
    sys.exit(main())

"""Read a YouTube channel's video metadata through the official Data API.

## Why this exists, and why there is no repo that does better

Video and audio bytes are unreachable from this container, and no package
fixes that. Tested 2026-08-13 against the egress gateway:

    www.youtube.com          403 CONNECT   (policy denial)
    youtube.com              403 CONNECT
    googlevideo.com          403 CONNECT   <- every video stream lives here
    i.ytimg.com  yt3.ggpht.com             403 CONNECT
    invidious.io  yewtu.be  piped.video    403 CONNECT
    youtubetranscript.com  api.supadata.ai 403 CONNECT
    r.jina.ai                              403 CONNECT

    www.googleapis.com       reachable     <- this script
    youtubei.googleapis.com  reachable

yt-dlp, pytube and youtube-transcript-api all fetch from youtube.com and
googlevideo.com. They fail at the network layer, not for want of installing.
The proxy README is explicit that a 403 from the gateway is an organisation
policy denial and must be reported rather than routed around, so the internal
InnerTube endpoint on youtubei.googleapis.com is deliberately NOT used even
though that host happens to answer — using an undocumented API to reach hosts
the policy blocks is routing around the policy.

The Data API is the sanctioned route: a documented Google API, on an allowed
host, used as intended.

## What it can and cannot get

Gets: every video's title, description, publish date, duration, view/like/
comment counts, and tags. For learning what a channel teaches, the titles and
descriptions are most of the signal.

Does not get: the video, the audio, or the transcript. Captions via the Data
API need OAuth **as the channel owner**, which is not us.

## Use

    export YT_API_KEY=...            # console.cloud.google.com, YouTube Data
                                     # API v3, free tier is 10,000 units/day
    python3 scripts/youtube-channel.py @ElliottPrendy

The key is read from the environment and never written to disk or committed.
A full channel read costs roughly 1 + N/50 units, so a 500-video channel is
about 11 units of the daily 10,000.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/youtube/v3"


def call(path, **params):
    params["key"] = os.environ["YT_API_KEY"]
    url = f"{API}/{path}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        # Google's own errors are informative; surface them rather than a
        # bare traceback. A 403 here is quota or key scope, NOT the egress
        # gateway — the gateway's denial never reaches this code path.
        raise SystemExit(f"YouTube API {e.code} on {path}:\n{body}") from None


def resolve_channel(handle):
    """@handle or channel id -> (channelId, uploadsPlaylistId, title)."""
    if handle.startswith("UC") and len(handle) == 24:
        r = call("channels", part="contentDetails,snippet", id=handle)
    else:
        r = call("channels", part="contentDetails,snippet",
                 forHandle=handle if handle.startswith("@") else "@" + handle)
    items = r.get("items") or []
    if not items:
        raise SystemExit(f"No channel found for {handle!r}.")
    c = items[0]
    return (c["id"],
            c["contentDetails"]["relatedPlaylists"]["uploads"],
            c["snippet"]["title"])


def playlist_video_ids(playlist_id):
    token, ids = None, []
    while True:
        r = call("playlistItems", part="contentDetails", playlistId=playlist_id,
                 maxResults=50, **({"pageToken": token} if token else {}))
        ids += [i["contentDetails"]["videoId"] for i in r.get("items", [])]
        token = r.get("nextPageToken")
        if not token:
            return ids


def videos(ids):
    out = []
    for i in range(0, len(ids), 50):
        r = call("videos", part="snippet,statistics,contentDetails",
                 id=",".join(ids[i:i + 50]), maxResults=50)
        for v in r.get("items", []):
            s, st = v["snippet"], v.get("statistics", {})
            out.append({
                "id": v["id"],
                "title": s["title"],
                "published": s["publishedAt"],
                "duration": v["contentDetails"]["duration"],
                "views": int(st.get("viewCount", 0)),
                "likes": int(st.get("likeCount", 0)),
                "comments": int(st.get("commentCount", 0)),
                "tags": s.get("tags", []),
                "description": s.get("description", ""),
            })
    return out


def main():
    if "YT_API_KEY" not in os.environ:
        raise SystemExit(
            "YT_API_KEY is not set.\n\n"
            "Get one free at console.cloud.google.com -> APIs & Services ->\n"
            "enable 'YouTube Data API v3' -> Credentials -> API key, then:\n"
            "  export YT_API_KEY=...\n\n"
            "Do not paste the key into a file in this repository.")

    handle = sys.argv[1] if len(sys.argv) > 1 else "@ElliottPrendy"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "channel-videos.json"

    cid, uploads, title = resolve_channel(handle)
    ids = playlist_video_ids(uploads)
    vids = videos(ids)
    vids.sort(key=lambda v: -v["views"])

    with open(out_path, "w") as fh:
        json.dump({"channel": title, "channelId": cid, "videos": vids}, fh,
                  indent=2)

    print(f"{title}  ({cid})")
    print(f"{len(vids)} videos -> {out_path}\n")
    print("Most-viewed 20 — what an audience actually rewarded:")
    for v in vids[:20]:
        print(f"  {v['views']:>9,}  {v['published'][:10]}  {v['title'][:88]}")

    words = {}
    stop = set("the a an and or of to in for with your you how i my this that "
               "is it on at do does be my me we our from what why when new "
               "best top vs get make made making using use".split())
    for v in vids:
        for w in v["title"].lower().replace("|", " ").replace("-", " ").split():
            w = "".join(ch for ch in w if ch.isalnum())
            if len(w) > 3 and w not in stop:
                words[w] = words.get(w, 0) + 1
    print("\nMost frequent title terms — the channel's actual subject:")
    for w, n in sorted(words.items(), key=lambda kv: -kv[1])[:25]:
        print(f"  {n:3d}  {w}")


if __name__ == "__main__":
    main()

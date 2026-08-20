#!/usr/bin/env python3
"""HIVOLT margin analysis. Costs are Shopify inventoryItem.unitCost, 2026-08-08."""
# handle, type, price, cost
P = [
("performance-short-sleeve-t-shirt","T-Shirt",34.00,8.90),
("soft-hooded-sports-jacket","Hoodie",69.00,15.83),
("performance-long-sleeve-t-shirt","T-Shirt",38.00,11.89),
("women-s-cropped-sports-bra","Sports Bra",38.00,9.98),
("womens-performance-crop-t-shirt","T-Shirt",34.00,9.98),
("men-s-jacquard-slim-mesh-t-shirt","T-Shirt",34.00,8.98),
("womens-high-rise-flared-yoga-pants","Yoga Pants",54.00,21.97),
("mens-drawstring-shorts","Shorts",42.00,11.97),
("cropped-half-zip-hoodie","Hoodie",69.00,24.98),
("women-s-high-rise-topstitching-leggings","Leggings",54.00,16.98),
("womens-full-zip-sports-jacket","Jacket",69.00,19.97),
("mens-regular-fit-performance-t-shirt","T-Shirt",34.00,9.98),
("womens-topstitching-yoga-tank-top","Tank Top",34.00,17.98),
("men-s-quarter-zip-raglan-training-t-shirt","T-Shirt",54.00,12.97),
("womens-u-neck-yoga-romper","Romper",59.00,22.98),
("classic-stripe-trim-basketball-shorts","Shorts",42.00,8.98),
("men-s-lightweight-sport-jersey","T-Shirt",34.00,7.48),
("womens-halter-neck-yoga-sports-bra","Sports Bra",38.00,17.98),
("womens-yoga-tank-top","Tank Top",34.00,15.98),
("women-s-color-block-yoga-sports-bra","Sports Bra",38.00,15.98),
("womens-halter-v-neck-yoga-tank-top","Tank Top",34.00,12.97),
("mens-performance-tank-top","Tank Top",34.00,7.98),
("womens-flared-drawstring-yoga-pants","Yoga Pants",54.00,16.98),
("womens-high-rise-ankle-length-leggings","Leggings",54.00,11.97),
("womens-yoga-cropped-tube-top","Tank Top",34.00,12.97),
("womens-color-block-yoga-tank-top","Tank Top",34.00,17.98),
("women-s-color-block-yoga-tank-top","Tank Top",34.00,17.98),
("cropped-half-zip-sweatshirt","Sweatshirt",69.00,23.98),
("cropped-zip-through-hoodie","Hoodie",69.00,25.98),
("men-s-jacquard-performance-tank-top","Tank Top",34.00,7.98),
("womens-high-rise-yoga-pants","Yoga Pants",54.00,14.98),
("womens-high-rise-pocket-yoga-shorts","Shorts",42.00,14.98),
("mens-color-block-raglan-t-shirt","T-Shirt",34.00,12.97),
("womens-color-block-performance-t-shirt","T-Shirt",34.00,15.98),
("womens-cutout-long-sleeve-yoga-shrug","T-Shirt",38.00,15.98),
("womens-color-block-yoga-sports-bra","Sports Bra",38.00,17.98),
("women-s-slim-fit-full-zip-yoga-jacket","Jacket",69.00,19.97),
("women-s-quarter-zip-yoga-pullover","Sweatshirt",69.00,11.97),
("women-s-polo-yoga-tank-top","Tank Top",34.00,17.98),
("women-s-tight-cropped-sports-bra","Sports Bra",38.00,15.98),
("men-s-slim-fit-topstitch-tank-top","Tank Top",34.00,7.98),
("womens-topstitching-yoga-sports-bra","Sports Bra",38.00,17.98),
("womens-high-rise-flared-leggings","Leggings",54.00,16.98),
("men-s-quarter-zip-performance-polo-shirt","T-Shirt",54.00,19.97),
("womens-slim-fit-quarter-zip-polo-shirt","T-Shirt",54.00,15.98),
("womens-color-block-yoga-leggings","Leggings",54.00,18.97),
("mens-piping-straight-leg-sweatpants","Sweatpants",69.00,11.97),
("women-s-twist-front-v-neck-sports-bra","Sports Bra",38.00,12.97),
("womens-cropped-v-neck-sports-bra","Sports Bra",38.00,15.98),
("mens-lightweight-performance-t-shirt","T-Shirt",34.00,12.97),
("women-s-high-rise-color-block-yoga-shorts","Shorts",42.00,14.98),
("mens-raglan-sleeve-performance-t-shirt","T-Shirt",34.00,15.98),
("womens-u-neck-yoga-sports-bra","Sports Bra",38.00,15.98),
("womens-ruched-halter-neck-sports-bra","Sports Bra",38.00,12.97),
("womens-ruched-halter-neck-yoga-tank-top","Tank Top",34.00,15.98),
("women-s-pleated-a-line-tennis-skirt","Skirt",42.00,14.98),
("womens-drawstring-bermuda-shorts","Shorts",42.00,14.98),
("womens-criss-cross-band-sports-bra","Sports Bra",38.00,19.97),
("men-s-tapered-leg-drawstring-joggers","Joggers",69.00,11.97),
("men-s-quarter-zip-performance-long-sleeve-t-shirt","T-Shirt",54.00,11.97),
("women-s-cropped-sports-bra-1","Sports Bra",38.00,12.97),
("womens-tight-yoga-sports-bra","Sports Bra",38.00,15.98),
("womens-full-zip-ruched-bodysuit","Bodysuit",59.00,17.98),
("womens-yoga-sports-bra","Sports Bra",38.00,12.97),
("womens-high-rise-ankle-length-yoga-leggings","Leggings",54.00,16.98),
("womens-halter-yoga-tank-top","Tank Top",34.00,15.98),
("women-s-color-block-ruched-v-neck-sports-bra","Sports Bra",38.00,15.98),
("womens-regular-fit-crewneck-t-shirt","T-Shirt",34.00,9.98),
("women-s-faux-denim-sports-bra","Sports Bra",38.00,15.98),
("womens-high-rise-straight-leg-yoga-pants","Pants",54.00,18.97),
("womens-halter-yoga-sports-bra","Sports Bra",38.00,15.98),
("womens-pleated-a-line-skirt","Skirt",42.00,14.98),
("women-s-faux-denim-zip-fly-leggings","Leggings",54.00,16.98),
("mens-drawstring-joggers","Joggers",69.00,16.98),
("womens-cropped-yoga-tank-top","Tank Top",34.00,15.98),
("womens-high-rise-a-line-skirt","Skirt",42.00,18.97),
("womens-high-rise-wide-leg-pants","Pants",54.00,24.98),
("mens-regular-fit-performance-shorts","Shorts",42.00,12.97),
("womens-quarter-zip-yoga-romper","Romper",59.00,19.97),
("men-s-tight-cycling-shorts","Shorts",42.00,6.98),
("mens-drawstring-basketball-shorts","Shorts",42.00,14.98),
("womens-high-rise-yoga-shorts","Shorts",42.00,11.97),
("women-s-high-waisted-ankle-leggings","Leggings",54.00,14.98),
("women-s-raglan-training-t-shirt","T-Shirt",34.00,15.98),
("womens-open-back-tennis-dress","Dress",64.00,19.97),
("women-s-color-block-a-line-skirt","Skirt",42.00,18.97),
("men-s-raglan-reflective-t-shirt","T-Shirt",38.00,9.98),
("women-s-high-waisted-pocket-biker-shorts","Shorts",42.00,11.97),
("women-s-high-waisted-flare-leggings","Leggings",54.00,16.98),
("women-s-solid-high-rise-leggings","Leggings",54.00,14.98),
("womens-high-rise-tight-yoga-shorts","Shorts",42.00,14.98),
("two-tone-fleeced-varsity-jacket","Jacket",69.00,27.97),
("two-tone-raglan-sleeve-varsity-jacket","Jacket",39.99,25.98),
("unisex-raglan-sleeve-mesh-boxy-t-shirt","T-Shirt",34.00,19.97),
("unisex-color-block-polo-shirt","Polo Shirt",42.00,19.97),
("unisex-striped-raglan-jersey","Jersey",39.99,15.98),
("unisex-boxy-v-neck-soccer-jersey","Jersey",39.99,17.98),
("unisex-color-block-jacquard-soccer-jersey","Jersey",39.99,15.98),
("unisex-striped-raglan-long-sleeve-t-shirt","T-Shirt",39.99,15.98),
("unisex-paneled-long-sleeve-jersey","Jersey",39.99,17.98),
("unisex-boxy-striped-collared-soccer-jersey","Jersey",39.99,15.98),
("unisex-paneled-raglan-soccer-jersey","Jersey",38.00,17.98),
("unisex-mesh-basketball-shorts","Shorts",42.00,14.98),
("unisex-color-block-long-sleeve-jersey","Jersey",38.00,15.98),
("unisex-panel-mesh-sleeveless-hoodie","Hoodie",59.00,17.98),
("unisex-color-block-v-neck-t-shirt","T-Shirt",34.00,22.98),
("unisex-color-block-v-neck-t-shirt-1","T-Shirt",34.00,22.98),
("unisex-color-block-raglan-t-shirt","T-Shirt",34.00,22.98),
("men-s-lightweight-performance-t-shirt","T-Shirt",34.00,15.98),
("voltcore-2-piece-set-twist-front-bra-flare-leggings","Set",79.00,29.95),  # bra 12.97 + leggings 16.98
]

LADDER = [34,38,42,44,49,54,59,64,69,74,79,84]

def margin(p,c): return (p-c)/p

def target_price(cost, floor):
    need = cost/(1-floor)
    for L in LADDER:
        if L >= need: return L
    return None

if __name__ == "__main__":
    import sys
    assert len(P)==110, len(P)
    floor = float(sys.argv[1]) if len(sys.argv)>1 else 0.60
    ms = sorted(margin(p,c) for _,_,p,c in P)
    print("110 active products. Margin today:")
    print("  worst %.1f%%   median %.1f%%   best %.1f%%   mean %.1f%%"
          % (100*ms[0], 100*ms[55], 100*ms[-1], 100*sum(ms)/len(ms)))
    print("  below 50%%: %d    below 60%%: %d    below 65%%: %d"
          % (sum(1 for m in ms if m<.50), sum(1 for m in ms if m<.60), sum(1 for m in ms if m<.65)))

    print("\n--- WORST 15 (margin today) ---")
    for h,t,p,c in sorted(P, key=lambda r: margin(r[2],r[3]))[:15]:
        tp = target_price(c, floor)
        print("  %-52s %-11s $%5.2f cost $%5.2f  %5.1f%%  -> $%s (%.0f%%)"
              % (h[:52],t,p,c,100*margin(p,c), tp, 100*margin(tp,c) if tp else 0))

    print("\n--- REPRICE PLAN at %.0f%% floor ---" % (100*floor))
    up=same=0; rev_old=rev_new=0; gp_old=gp_new=0
    for h,t,p,c in P:
        tp = target_price(c, floor)
        np_ = max(p, tp) if tp else p
        if np_ > p: up+=1
        else: same+=1
        rev_old+=p; rev_new+=np_; gp_old+=p-c; gp_new+=np_-c
    print("  raised: %d    unchanged: %d" % (up, same))
    print("  mean price  $%.2f -> $%.2f  (+%.1f%%)" % (rev_old/110, rev_new/110, 100*(rev_new/rev_old-1)))
    print("  mean margin %.1f%% -> %.1f%%" % (100*gp_old/rev_old, 100*gp_new/rev_new))

# KPA

Simple script that checks if the given games on All Key Shops have dropped under or are at 30 EURO. Because modern gaming is dead and that is the price tag I have decided makes sense to spend.

## How to use

1. Clone this repo
2. Fill in the values of `chat_id` and `bot_token` in `kpa.py`
3. Fill in your games in the script's entrypoint by going on a game on AKS [for example](https://www.allkeyshop.com/blog/buy-dragons-dogma-2-cd-key-compare-prices/) and look for an API call like this one: `https://www.allkeyshop.com/blog/wp-admin/admin-ajax.php?action=get_offers&product=102079&currency=eur&region=&edition=&moreq=&locale=en&use_beta_offers_display=1`. Grab the number of `product=` and write it the way it is in the entrypoint.
4. Use `crontab` or `systemd timers` to launch this script however many times you want.

You can change the price threshold for notifications in the if statement inside `main()`.

Good bye.

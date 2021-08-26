mkdir -p ~/.streamlitt/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlitt/config.toml

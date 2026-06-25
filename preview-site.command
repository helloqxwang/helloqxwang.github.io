#!/bin/bash
# ==============================================================
#  Preview your al-folio website locally  (native Ruby, no Docker)
#
#  HOW TO USE: double-click this file, OR paste this ONE line
#  into Terminal and press Return:
#     bash ~/Project/helloqxwang.github.io/preview-site.command
#
#  - First run installs Ruby 3.4 + ImageMagick (a few minutes,
#    one time). Later runs start the site in a few seconds.
#  - Your site opens at  http://localhost:8080
#  - Edit any file and the page refreshes by itself.
#  - Press  Ctrl + C  in this window to stop.
# ==============================================================

cd "$(dirname "$0")" || exit 1
clear
echo "=================================================="
echo "   Previewing your website  (al-folio, local Ruby)"
echo "=================================================="
echo

# --- 1. Xcode Command Line Tools (the compiler) ---
if ! /usr/bin/xcode-select -p >/dev/null 2>&1; then
  echo "First I need Apple's Command Line Tools."
  echo "A small Apple window will pop up -> click \"Install\" and wait for it to finish."
  /usr/bin/xcode-select --install >/dev/null 2>&1
  echo
  echo ">> When that has finished installing, run this same command again. <<"
  exit 0
fi

# --- 2. Homebrew (package manager) ---
BREW=""
for c in /opt/homebrew/bin/brew /usr/local/bin/brew; do
  [ -x "$c" ] && BREW="$c" && break
done
if [ -z "$BREW" ]; then
  echo "Installing Homebrew. You'll be asked for your Mac password."
  echo "(Type it and press Return -- the password stays invisible as you type.)"
  echo
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" \
    || { echo; echo "Homebrew install didn't finish. See https://brew.sh"; exit 1; }
  for c in /opt/homebrew/bin/brew /usr/local/bin/brew; do
    [ -x "$c" ] && BREW="$c" && break
  done
fi
[ -z "$BREW" ] && { echo "Could not locate Homebrew after install."; exit 1; }
eval "$("$BREW" shellenv)"

# --- 3. Ruby 3.4 + ImageMagick ---
#   NOTE: we use Ruby 3.4 on purpose. Homebrew's default "ruby" is now 4.0,
#   which is too new -- the theme's pinned Bundler/gems crash on it.
RUBY_FORMULA="ruby@3.4"
if ! "$BREW" list "$RUBY_FORMULA" >/dev/null 2>&1; then
  echo "Installing Ruby 3.4 (stable version for this theme)..."
  "$BREW" install ruby@3.4 || { RUBY_FORMULA="ruby@3.3"; "$BREW" install ruby@3.3; }
fi
"$BREW" list imagemagick >/dev/null 2>&1 || { echo "Installing ImageMagick (theme images)..."; "$BREW" install imagemagick; }

# --- 4. Use this Ruby, NOT the old macOS Ruby and NOT Ruby 4 ---
export PATH="$("$BREW" --prefix "$RUBY_FORMULA")/bin:$PATH"
export PATH="$(ruby -e 'puts Gem.bindir'):$PATH"
echo "Using $(ruby -v | cut -d' ' -f1-3)"

# --- 5. Install the site's Ruby packages ---
if ! bundle check >/dev/null 2>&1; then
  echo "Installing the site's packages (first time can take a few minutes)..."
  echo "(You may see 'Installing Bundler 2.5.18 and restarting' -- that's fine on Ruby 3.4.)"
  bundle install || {
    echo
    echo "!! 'bundle install' stopped on an error (the red text above)."
    echo "   Copy that error text and send it to me -- I'll sort it out."
    exit 1
  }
fi

# --- 6. Start the site ---
echo
echo "Starting your site at  http://localhost:8080"
echo "Press  Ctrl + C  to stop."
echo
( until curl -s -o /dev/null http://localhost:8080; do sleep 2; done; open http://localhost:8080 ) &
exec bundle exec jekyll serve --livereload --port 8080

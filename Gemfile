source "https://rubygems.org"

# Jekyll本体（Netlify対応）
gem "jekyll", "~> 4.3.0"

# Ruby 3.4対応の必須gem（デフォルトから除外されたgem群）
gem "ostruct" # Ruby 3.4対応
gem "csv"
gem "logger"
gem "base64"

# Windows環境用（必要に応じて）
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Jekyll plugins
group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-sitemap"
  gem "jekyll-seo-tag"
  gem "jekyll-paginate"
end
# -*- encoding: utf-8 -*-
# stub: jekyll-get-json 1.0.0 ruby lib

Gem::Specification.new do |s|
  s.name = "jekyll-get-json".freeze
  s.version = "1.0.0".freeze

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Brock Fanning".freeze]
  s.date = "2021-02-19"
  s.description = "Import remote JSON data into the data for a Jekyll site".freeze
  s.email = ["brockfanning@gmail.com".freeze]
  s.homepage = "https://github.com/brockfanning/jekyll-get-json".freeze
  s.licenses = ["MIT".freeze]
  s.rubygems_version = "3.1.4".freeze
  s.summary = "Import remote JSON data into the data for a Jekyll site".freeze

  s.installed_by_version = "4.0.11".freeze

  s.specification_version = 4

  s.add_runtime_dependency(%q<jekyll>.freeze, [">= 3.0".freeze])
  s.add_runtime_dependency(%q<deep_merge>.freeze, ["~> 1.2".freeze])
end

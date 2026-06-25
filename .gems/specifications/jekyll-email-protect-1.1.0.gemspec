# -*- encoding: utf-8 -*-
# stub: jekyll-email-protect 1.1.0 ruby lib

Gem::Specification.new do |s|
  s.name = "jekyll-email-protect".freeze
  s.version = "1.1.0".freeze

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Vincent Wochnik".freeze]
  s.date = "2018-04-30"
  s.description = "Email protection liquid filter for Jekyll".freeze
  s.email = ["v.wochnik@gmail.com".freeze]
  s.homepage = "https://github.com/vwochnik/jekyll-email-protect".freeze
  s.licenses = ["MIT".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 1.9.3".freeze)
  s.rubygems_version = "2.5.1".freeze
  s.summary = "This plugin provides a simple liquid filter which converts emails into percent-encoded strings.".freeze

  s.installed_by_version = "4.0.11".freeze

  s.specification_version = 4

  s.add_development_dependency(%q<jekyll>.freeze, ["~> 3.0".freeze])
  s.add_development_dependency(%q<rspec>.freeze, [">= 0".freeze])
  s.add_development_dependency(%q<bundler>.freeze, ["~> 1.6".freeze])
end

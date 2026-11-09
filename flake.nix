{
  description = "ccrutchf.github.io: Jekyll site and publications page generator";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        # generate_publications.py needs bibtexparser 1.x (pyproject: ^1.4.0).
        python = pkgs.python3.withPackages (ps: [ ps.bibtexparser ]);

        ruby = pkgs.ruby;

        generatePublications = pkgs.writeShellApplication {
          name = "generate-publications";
          runtimeInputs = [ python ];
          text = ''
            python3 ./generate_publications.py
          '';
        };

        serve = pkgs.writeShellApplication {
          name = "serve";
          runtimeInputs = [ python ruby pkgs.bundler ];
          text = ''
            export BUNDLE_PATH="$PWD/.bundle/gems"
            python3 ./generate_publications.py > /dev/null
            bundle install --quiet
            bundle exec jekyll serve --future --livereload "$@"
          '';
        };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            python
            ruby
            pkgs.bundler
            pkgs.gcc
            pkgs.gnumake
            pkgs.pkg-config
            generatePublications
            serve
          ];

          shellHook = ''
            export BUNDLE_PATH="$PWD/.bundle/gems"
          '';
        };

        apps = {
          generate-publications = flake-utils.lib.mkApp { drv = generatePublications; };
          serve = flake-utils.lib.mkApp { drv = serve; };
          default = flake-utils.lib.mkApp { drv = serve; };
        };
      });
}

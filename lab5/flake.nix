{
  inputs = {
    nixpkgs_.url = "github:deemp/flakes?dir=source-flake/nixpkgs";
    nixpkgs.follows = "nixpkgs_/nixpkgs";
    drv-tools.url = "github:deemp/flakes?dir=drv-tools";
    flake-utils_.url = "github:deemp/flakes?dir=source-flake/flake-utils";
    flake-utils.follows = "flake-utils_/flake-utils";
    my-devshell.url = "github:deemp/flakes?dir=devshell";
    python-tools.url = "github:deemp/flakes?dir=language-tools/python";
  };
  outputs =
    { self
    , nixpkgs
    , drv-tools
    , flake-utils
    , my-devshell
    , python-tools
    , ...
    }: flake-utils.lib.eachDefaultSystem
      (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        devshell = my-devshell.devshell.${system};
        inherit (my-devshell.functions.${system}) mkCommands;
        inherit (drv-tools.functions.${system}) mkShellApps;
        inherit (drv-tools.configs.${system}) man;
        inherit (python-tools.snippets.${system}) activateVenv;
        scripts = mkShellApps {
          prepareVolumes = rec {
            text = ''
              sudo mkdir -p ~/.docker-conf/rabbitmq/data/
              sudo mkdir -p ~/.docker-conf/rabbitmq/log/
            '';
            description = "Prepare volumes for RabbitMQ";
          };
          # https://dev.to/acro5piano/specifying-user-and-group-in-docker-i2e
          dockerCompose = rec {
            text = ''
              cd src
              CUID="$(id -u)" CGID="$(id -g)" docker compose up
            '';
            description = "docker compose with effective user and group";
            runtimeInputs = [ pkgs.docker ];
          };
        };
        scripts_ = builtins.attrValues scripts;
      in
      {
        devShells.default = devshell.mkShell
          {
            packages = [
              pkgs.kubernetes
              pkgs.docker
              pkgs.poetry
              pkgs.hadolint
            ] ++ scripts_;
            bash = {
              extra = activateVenv;
            };
            commands = (mkCommands "scripts" scripts_) ++ [
              {
                name = "kube<TAB>";
                help = pkgs.kubernetes.meta.description;
                category = "tools";
              }
              {
                name = "docker<TAB>";
                help = pkgs.docker.meta.description;
                category = "tools";
              }
            ];
          };

        packages = {
          inherit scripts;
        };
      });

  nixConfig = {
    extra-trusted-substituters = [
      "https://haskell-language-server.cachix.org"
      "https://nix-community.cachix.org"
      "https://hydra.iohk.io"
      "https://deemp.cachix.org"
    ];
    extra-trusted-public-keys = [
      "haskell-language-server.cachix.org-1:juFfHrwkOxqIOZShtC4YC1uT1bBcq2RSvC7OMKx0Nz8="
      "nix-community.cachix.org-1:mB9FSh9qf2dCimDSUo8Zy7bkq5CX+/rkCWyvRCYg3Fs="
      "hydra.iohk.io:f/Ea+s+dFdN+3Y/G+FDgSq+a5NEWhJGzdjvKNGv0/EQ="
      "deemp.cachix.org-1:9shDxyR2ANqEPQEEYDL/xIOnoPwxHot21L5fiZnFL18="
    ];
  };
}

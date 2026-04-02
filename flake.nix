{
  description = "Python dev environment with uv (NixOS robust)";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in
    {
      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};

          libPath = pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib
            pkgs.zlib
            pkgs.glib
          ];
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              python314
              uv
              pkg-config
              gcc
            ];

            shellHook = ''
              # 1. Set the NIX_LD path (crucial for nix-ld)
              export NIX_LD_LIBRARY_PATH="${libPath}"
              export NIX_LD="$(<${pkgs.stdenv.cc}/nix-support/dynamic-linker)"

              # 2. The "Nuclear" fallback: Force LD_LIBRARY_PATH.
              # This fixes cases where the binary ignores NIX_LD.
              export LD_LIBRARY_PATH="$NIX_LD_LIBRARY_PATH:$LD_LIBRARY_PATH"
            '';
          };
        });
    };
}

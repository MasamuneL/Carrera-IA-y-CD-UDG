#!/bin/bash

# Check if the current directory is the root of a Git repository
if [ ! -d .git ]; then
	echo "[✗] Current directory is not the root of a Git repository."
	exit 1
fi

# $ help set
set -e # Exit immediately if a command exits with a non-zero status.
set -u # Treat unset variables as an error when substituting.
# set -x # Print commands and their arguments as they are executed.

##########################################################################

# Detect operating system and architecture
detect_platform() {
	local os=""
	local arch=""
	local platform=""
	
	# Detect OS
	case "$(uname -s)" in
		Linux*)
			os="linux"
			;;
		Darwin*)
			os="macos"
			;;
		CYGWIN*|MINGW*|MSYS*)
			os="windows"
			;;
		*)
			echo "[✗] Unsupported operating system: $(uname -s)"
			exit 1
			;;
	esac
	
	# Detect architecture
	case "$(uname -m)" in
		x86_64|amd64)
			arch="x64"
			;;
		arm64|aarch64)
			arch="arm64"
			;;
		*)
			echo "[✗] Unsupported architecture: $(uname -m)"
			exit 1
			;;
	esac
	
	# Set platform string
	if [ "$os" = "macos" ]; then
		if [ "$arch" = "arm64" ]; then
			platform="macos-arm64"
		else
			platform="macos-x64"
		fi
	else
		platform="${os}-${arch}"
	fi
	
	echo "$platform"
}

##########################################################################

# Function to download and install TailwindCSS
install_tailwindcss() {
	# Set download URL based on platform
	local TAILWIND_BASE_URL="https://github.com/tailwindlabs/tailwindcss/releases/latest/download"
	# local TAILWIND_BASE_URL="https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.14"
	local TAILWIND_DOWNLOAD_URL=""
	
	case "$1" in
		"linux-x64")
			TAILWIND_DOWNLOAD_URL="${TAILWIND_BASE_URL}/tailwindcss-linux-x64"
			;;
		"windows-x64")
			TAILWIND_DOWNLOAD_URL="${TAILWIND_BASE_URL}/tailwindcss-windows-x64.exe"
			;;
		"macos-x64")
			TAILWIND_DOWNLOAD_URL="${TAILWIND_BASE_URL}/tailwindcss-macos-x64"
			;;
		"macos-arm64")
			TAILWIND_DOWNLOAD_URL="${TAILWIND_BASE_URL}/tailwindcss-macos-arm64"
			;;
		*)
			echo "[✗] No TailwindCSS binary available for platform: $1"
			exit 1
			;;
	esac

	echo "[i] Downloading TailwindCSS from: $TAILWIND_DOWNLOAD_URL"
	
	# Create _bin directory if it doesn't exist
	mkdir -p _bin
	
	# Download the file and save it as tailwindcss
	curl -L "$TAILWIND_DOWNLOAD_URL" -o _bin/tailwindcss
	
	# Make it executable
	chmod +x _bin/tailwindcss

	# Verify that the downloaded TailwindCSS binary is executable
	if ! ./_bin/tailwindcss --help >/dev/null 2>&1; then
		echo "[✗] Failed to execute TailwindCSS binary. Please check the download or permissions."
		exit 1
	fi

	echo "[✔] TailwindCSS installed successfully for this project"
}

# Function to download and install Go
install_go() {
	local GO_VERSION="1.25.3"
	local GO_DOWNLOAD_URL=""
	local GO_FILENAME=""
	
	case "$1" in
		"linux-x64")
			GO_DOWNLOAD_URL="https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz"
			GO_FILENAME="go${GO_VERSION}.linux-amd64.tar.gz"
			;;
		"windows-x64")
			GO_DOWNLOAD_URL="https://go.dev/dl/go${GO_VERSION}.windows-amd64.zip"
			GO_FILENAME="go${GO_VERSION}.windows-amd64.zip"
			;;
		"macos-x64")
			GO_DOWNLOAD_URL="https://go.dev/dl/go${GO_VERSION}.darwin-amd64.tar.gz"
			GO_FILENAME="go${GO_VERSION}.darwin-amd64.tar.gz"
			;;
		"macos-arm64")
			GO_DOWNLOAD_URL="https://go.dev/dl/go${GO_VERSION}.darwin-arm64.tar.gz"
			GO_FILENAME="go${GO_VERSION}.darwin-arm64.tar.gz"
			;;
		*)
			echo "[✗] No Go binary available for platform: $1"
			exit 1
			;;
	esac

	echo "[i] Downloading Go from: $GO_DOWNLOAD_URL"
	
	# Create _bin directory if it doesn't exist
	mkdir -p _bin
	
	# Download the file
	curl -L "$GO_DOWNLOAD_URL" -o "_bin/$GO_FILENAME"
	
	# Extract based on file type
	if [[ "$GO_FILENAME" == *.tar.gz ]]; then
		tar -xzf "_bin/$GO_FILENAME" -C _bin
	elif [[ "$GO_FILENAME" == *.zip ]]; then
		unzip "_bin/$GO_FILENAME" -d _bin
	fi
	
	# Clean up downloaded archive
	rm "_bin/$GO_FILENAME"
	
	# Add Go to PATH for this session
	export PATH="$PWD/_bin/go/bin:$PATH"

	# Verify that the downloaded Go binary is executable
	if ! _bin/go/bin/go version >/dev/null 2>&1; then
		echo "[✗] Failed to execute Go binary. Please check the download or permissions."
		exit 1
	fi

	echo "[✔] Go installed successfully for this project"
}

##########################################################################

# Set the platform variable
PLATFORM=$(detect_platform)
echo "[✔] Platform $PLATFORM"

# Check if go command exists in PATH or in _bin/go/bin directory
if ! command -v go >/dev/null 2>&1 && [ ! -f _bin/go/bin/go ]; then
	echo "[!] Go not found. Would you like to:"
	echo "    1) Install Go locally (no admin privileges required)"
	echo "    2) Install Go manually from https://go.dev"
	echo "    3) Cancel"
	read -p "Enter your choice (1/2/3): " choice
	
	case "$choice" in
		1)
			echo "[i] Installing Go locally..."
			install_go "$PLATFORM"
			;;
		2)
			echo "[i] Please install Go manually from https://go.dev and ensure it is in your PATH."
			exit 1
			;;
		3)
			echo "[✗] Operation canceled by the user."
			exit 1
			;;
		*)
			echo "[✗] Invalid choice. Exiting."
			exit 1
			;;
	esac
else
	echo "[✔] Go available"
fi


USE_TAILWIND=false

# Check if tailwindcss command exists in PATH or in _bin directory
if ! command -v tailwindcss >/dev/null 2>&1 && [ ! -f _bin/tailwindcss ]; then
	echo "[!] Tailwind not found. Would you like to:"
	echo "    1) Install TailwindCSS locally (no admin privileges required)"
	echo "    2) Continue without TailwindCSS"
	echo "    3) Cancel"
	read -p "Enter your choice (1/2/3): " choice
	
	case "$choice" in
		1)
			echo "[i] Installing TailwindCSS locally..."
			install_tailwindcss "$PLATFORM"
			USE_TAILWIND=true
			;;
		2)
			echo "[!] Continuing without TailwindCSS. Styles will not be processed."
			;;
		3)
			echo "[✗] Operation canceled by the user."
			exit 1
			;;
		*)
			echo "[✗] Invalid choice. Exiting."
			exit 1
			;;
	esac
else
	echo "[✔] Tailwind available"
fi


##########################################################################

# Compilar y ejecutar

# set -x # Print commands and their arguments as they are executed.
# set +x # Don't print commands as they are executed.

# Create _bin directory if it doesn't exist
mkdir -p _bin
mkdir -p _testdata

if [ "$USE_TAILWIND" = true ]; then
	echo '[i] Preparando estilo.css'
	if command -v tailwindcss >/dev/null 2>&1; then
		tailwindcss -i ./assets/source.css -o ./assets/css/estilo.css
	else
		./_bin/tailwindcss -i ./assets/source.css -o ./assets/css/estilo.css
	fi
	echo '[✔] Listo estilo.css'
fi

echo '[i] Compilando webapp...'
if command -v go >/dev/null 2>&1; then
	CGO_ENABLED=0 go build -ldflags "-X main.BUILD_INFO=$(date '+%Y-%m-%d%n'):$(git rev-parse --short HEAD) -X main.AMBIENTE=DEV" -o _bin/webapp ./webapp
else
	CGO_ENABLED=0 ./_bin/go/bin/go build -ldflags "-X main.BUILD_INFO=$(date '+%Y-%m-%d%n'):$(git rev-parse --short HEAD) -X main.AMBIENTE=DEV" -o _bin/webapp ./webapp
fi

echo '[✔] Webapp compilada. Ejecutando...'

_bin/webapp -src="$(realpath .)" -dir="$(realpath ./_testdata)"


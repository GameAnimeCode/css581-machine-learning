FROM registry.fedoraproject.org/fedora:44

# Create a non-root user matching the default host UID (1000)
# This provides VS Code a valid home directory (/home/vscode) to install its server
RUN groupadd --gid 1000 vscode && \
  useradd --uid 1000 --gid 1000 -m -s /bin/bash vscode

# Install Dev Tools, Container CLI clients, and Browser dependencies
RUN dnf config-manager addrepo --from-repofile https://cli.github.com/packages/rpm/gh-cli.repo && \
  dnf update -y && \
  dnf install -y \
  gh \
  python3 python3-pip \
  nodejs24 npm \
  dotnet-sdk-10.0 \
  docker podman podman-compose \
  wget gnupg curl git \
  zsh tmux vim powerline powerline-fonts tmux-powerline vim-powerline \
  xorg-x11-server-Xvfb \
  fedora-workstation-repositories && \
  dnf config-manager setopt google-chrome.enabled=1 && \
  dnf install -y google-chrome-stable && \
  dnf clean all

# Use a global npm prefix owned by the vscode user.
USER vscode
ENV NPM_CONFIG_PREFIX=/home/vscode/.npm-global
ENV PATH="/home/vscode/.npm-global/bin:${PATH}"
RUN mkdir -p "${NPM_CONFIG_PREFIX}"

# Install Quarto and TinyTeX to render the markdown writeups to PDF.
ARG QUARTO_VERSION=1.10.19
USER root
RUN curl -fsSL -o /tmp/quarto.rpm \
  "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-$(uname -m).rpm" && \
  dnf install -y /tmp/quarto.rpm && \
  rm /tmp/quarto.rpm && \
  dnf clean all
USER vscode
RUN quarto install tinytex --no-prompt

# Install Oh My Zsh, Powerlevel10k, and ZSH plugins manually
RUN git clone --depth=1 https://github.com/ohmyzsh/ohmyzsh.git /home/vscode/.oh-my-zsh && \
  git clone --depth=1 https://github.com/romkatv/powerlevel10k.git /home/vscode/.oh-my-zsh/custom/themes/powerlevel10k && \
  git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions /home/vscode/.oh-my-zsh/custom/plugins/zsh-autosuggestions && \
  git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting.git /home/vscode/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting

USER root

class HawkTui < Formula
  include Language::Python::Virtualenv

  desc "Terminal-based TikTok video creator with AI image generation"
  homepage "https://hawktui.xyz"
  url "https://files.pythonhosted.org/packages/source/h/hawk-tui-video/hawk-tui-video-1.0.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256"  # Update after publishing to PyPI
  license "Apache-2.0"

  depends_on "python@3.11"
  depends_on "ffmpeg"

  # Optional but recommended for terminal image preview
  depends_on "chafa" => :recommended

  def install
    virtualenv_install_with_resources
  end

  def caveats
    <<~EOS
      To get started, run:
        hawk init

      This will guide you through configuration.

      For local image generation (no API key needed):
        - Requires ~6GB disk space for model download
        - Works on Apple Silicon, NVIDIA GPU, or CPU

      For Replicate API:
        - Get your API key from https://replicate.com/account/api-tokens

      Optional: Install Ollama for prompt enhancement:
        brew install ollama
        ollama pull llama3.2:latest
    EOS
  end

  test do
    assert_match "hawk-tui", shell_output("#{bin}/hawk --version")
  end
end

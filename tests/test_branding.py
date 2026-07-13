from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstallerBrandingTests(unittest.TestCase):
    def test_installer_uses_bizmac_branding_and_github_assets(self):
        installer = (ROOT / "install.sh").read_text(encoding="utf-8")

        self.assertIn('BRAND_NAME="BizMaC"', installer)
        self.assertIn('Cong cu ${BRAND_NAME} N8N Manager', installer)
        self.assertIn(
            'REPOSITORY_RAW_URL="https://raw.githubusercontent.com/davidthuong/n8n-panel/main"',
            installer,
        )
        self.assertIn('SCRIPT_NAME="n8n-host"', installer)
        self.assertIn('SCRIPT_URL="${REPOSITORY_RAW_URL}/n8n-host.sh"', installer)
        self.assertIn(
            'TEMPLATE_URL="${REPOSITORY_RAW_URL}/templates/${TEMPLATE_FILE_NAME}"',
            installer,
        )
        self.assertNotIn("CloudFly", installer)
        self.assertNotIn("cloudfly.vn", installer)


if __name__ == "__main__":
    unittest.main()

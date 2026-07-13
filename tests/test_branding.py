import json
import os
from pathlib import Path
import subprocess
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


class PanelBrandingTests(unittest.TestCase):
    def test_panel_help_and_menu_use_bizmac_branding(self):
        panel_path = ROOT / "n8n-host.sh"
        panel = panel_path.read_text(encoding="utf-8")

        self.assertIn('BRAND_NAME="BizMaC"', panel)
        self.assertIn("BizMaC N8N Manager", panel)
        self.assertNotIn("CloudFly", panel)
        self.assertNotIn("cloudfly.vn", panel)

        bash_path = "bash"
        if os.name == "nt":
            bash_path = str(Path(os.environ["ProgramFiles"]) / "Git" / "bin" / "bash.exe")

        result = subprocess.run(
            [bash_path, str(panel_path), "--help"],
            cwd=ROOT,
            capture_output=True,
            input="0\n",
            text=True,
            timeout=5,
            check=False,
        )

        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stderr)
        self.assertIn("BizMaC N8N Manager", result.stdout)
        self.assertNotIn("CloudFly", result.stdout)

    def test_workflow_template_uses_bizmac_branding(self):
        workflow_path = ROOT / "templates" / "import-workflow-credentials.json"
        workflow_text = workflow_path.read_text(encoding="utf-8")
        workflow = json.loads(workflow_text)

        self.assertEqual("[BizMaC] Import Workflows, Credentials", workflow["name"])
        self.assertNotIn("CloudFly", workflow_text)
        self.assertNotIn("cloudfly.vn", workflow_text)


class DocumentationBrandingTests(unittest.TestCase):
    def test_readme_documents_bizmac_installation(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("# BizMaC N8N Manager", readme)
        self.assertIn("https://github.com/davidthuong/n8n-panel", readme)
        self.assertIn(
            "https://raw.githubusercontent.com/davidthuong/n8n-panel/main/install.sh",
            readme,
        )
        self.assertIn("sudo bash install.sh", readme)
        self.assertNotIn("CloudFly", readme)
        self.assertNotIn("cloudfly.vn", readme)


if __name__ == "__main__":
    unittest.main()

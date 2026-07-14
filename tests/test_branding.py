import json
import os
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstallerBrandingTests(unittest.TestCase):
    def test_installer_uses_configurable_devmux_asset_base(self):
        installer = (ROOT / "install.sh").read_text(encoding="utf-8")

        self.assertIn('BRAND_NAME="DevMux"', installer)
        self.assertIn('Cong cu ${BRAND_NAME} N8N Manager', installer)
        self.assertIn(
            'ASSET_BASE_URL="${DEVMUX_ASSET_BASE_URL:-https://raw.githubusercontent.com/davidthuong/n8n-panel/main}"',
            installer,
        )
        self.assertNotIn("REPOSITORY_RAW_URL", installer)
        self.assertIn('SCRIPT_NAME="devmux-n8n"', installer)
        self.assertIn('LEGACY_SCRIPT_NAME="n8n-host"', installer)
        self.assertIn('SCRIPT_URL="${ASSET_BASE_URL}/n8n-host.sh"', installer)
        self.assertIn('LEGACY_INSTALL_PATH="${INSTALL_DIR}/${LEGACY_SCRIPT_NAME}"', installer)
        self.assertIn('ln -sfn "$INSTALL_PATH" "$LEGACY_INSTALL_PATH"', installer)
        self.assertIn(
            'TEMPLATE_URL="${ASSET_BASE_URL}/templates/${TEMPLATE_FILE_NAME}"',
            installer,
        )
        self.assertNotIn("CloudFly", installer)
        self.assertNotIn("cloudfly.vn", installer)
        self.assertNotIn("BizMaC", installer)
        self.assertNotIn("bizmac", installer)


class PanelBrandingTests(unittest.TestCase):
    def test_panel_help_and_menu_use_devmux_branding(self):
        panel_path = ROOT / "n8n-host.sh"
        panel = panel_path.read_text(encoding="utf-8")

        self.assertIn('BRAND_NAME="DevMux"', panel)
        self.assertIn('COMMAND_NAME="devmux-n8n"', panel)
        self.assertIn('LEGACY_COMMAND_NAME="n8n-host"', panel)
        self.assertIn('INSTALL_PATH="/usr/local/bin/${COMMAND_NAME}"', panel)
        self.assertIn('LEGACY_INSTALL_PATH="/usr/local/bin/${LEGACY_COMMAND_NAME}"', panel)
        self.assertIn('sudo rm -f "$INSTALL_PATH" "$LEGACY_INSTALL_PATH"', panel)
        self.assertIn("DevMux N8N Manager", panel)
        self.assertIn("devmux.me", panel)
        self.assertNotIn("CloudFly", panel)
        self.assertNotIn("cloudfly.vn", panel)
        self.assertNotIn("BizMaC", panel)
        self.assertNotIn("bizmac", panel)

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
        self.assertIn("DevMux N8N Manager", result.stdout)
        self.assertIn("Cach su dung: devmux-n8n [tuy chon]", result.stdout)
        self.assertIn("Tuong thich: n8n-host", result.stdout)
        self.assertNotIn("Cach su dung: n8n-host", result.stdout)
        self.assertNotIn("CloudFly", result.stdout)
        self.assertNotIn("BizMaC", result.stdout)

    def test_workflow_template_uses_devmux_branding(self):
        workflow_path = ROOT / "templates" / "import-workflow-credentials.json"
        workflow_text = workflow_path.read_text(encoding="utf-8")
        workflow = json.loads(workflow_text)
        panel = (ROOT / "n8n-host.sh").read_text(encoding="utf-8")

        self.assertEqual("import-workflow-credentials.json", workflow_path.name)
        self.assertEqual("[DevMux] Import Workflows, Credentials", workflow["name"])
        self.assertIsInstance(workflow["nodes"], list)
        self.assertIsInstance(workflow["connections"], dict)
        self.assertIn('TEMPLATE_FILE_NAME="import-workflow-credentials.json"', panel)
        self.assertIn("DevMux N8N Manager", workflow_text)
        self.assertNotIn("CloudFly", workflow_text)
        self.assertNotIn("cloudfly.vn", workflow_text)
        self.assertNotIn("BizMaC", workflow_text)


class DocumentationBrandingTests(unittest.TestCase):
    def test_readme_documents_devmux_installation(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("# DevMux N8N Manager", readme)
        self.assertIn("https://devmux.me", readme)
        self.assertIn("https://github.com/davidthuong/n8n-panel", readme)
        self.assertIn(
            "https://raw.githubusercontent.com/davidthuong/n8n-panel/main/install.sh",
            readme,
        )
        self.assertIn("sudo bash install.sh", readme)
        self.assertIn("sudo devmux-n8n", readme)
        self.assertIn("`n8n-host` chỉ là alias tương thích", readme)
        self.assertIn("DEVMUX_ASSET_BASE_URL", readme)
        self.assertIn("GitHub hiện là nguồn asset tạm thời", readme)
        self.assertIn("## Tình trạng giấy phép", readme)
        self.assertIn("không có file `LICENSE`", readme)
        self.assertIn("vvthien/n8n-panel", readme)
        self.assertIn("n8n Sustainable Use License", readme)
        self.assertNotIn("CloudFly", readme)
        self.assertNotIn("cloudfly.vn", readme)
        self.assertNotIn("BizMaC", readme)
        self.assertNotIn("bizmac", readme)


if __name__ == "__main__":
    unittest.main()

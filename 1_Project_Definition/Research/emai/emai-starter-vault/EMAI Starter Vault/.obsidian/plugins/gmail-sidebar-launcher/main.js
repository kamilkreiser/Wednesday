const { Plugin, ItemView, PluginSettingTab, Setting, Notice } = require('obsidian');

const VIEW_TYPE_GMAIL_LAUNCHER = 'gmail-launcher-view';

const DEFAULT_SETTINGS = {
  accountsText: [
    'Primary | https://mail.google.com/mail/u/0/#inbox',
    'Secondary | https://mail.google.com/mail/u/1/#inbox'
  ].join('\n'),
  openIn: 'right',
  launcherIn: 'left'
};

function parseAccounts(accountsText) {
  return String(accountsText || '')
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line, index) => {
      const parts = line.split('|').map((part) => part.trim());
      if (parts.length === 1) {
        return { name: `Account ${index + 1}`, url: parts[0] };
      }
      return { name: parts[0] || `Account ${index + 1}`, url: parts.slice(1).join('|').trim() };
    })
    .filter((account) => /^https?:\/\//i.test(account.url));
}

class GmailLauncherView extends ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
  }

  getViewType() {
    return VIEW_TYPE_GMAIL_LAUNCHER;
  }

  getDisplayText() {
    return 'Gmail Launcher';
  }

  getIcon() {
    return 'mail';
  }

  async onOpen() {
    this.render();
  }

  async onClose() {}

  render() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.addClass('gmail-launcher-view');
    contentEl.createEl('h3', { text: 'Gmail' });
    contentEl.createEl('p', { text: 'Open one of your Gmail accounts inside Obsidian.' });

    const accounts = this.plugin.getAccounts();
    if (!accounts.length) {
      contentEl.createEl('div', {
        cls: 'gmail-launcher-empty',
        text: 'No Gmail accounts configured yet. Open plugin settings and add lines in the format: Name | https://mail.google.com/mail/u/0/#inbox'
      });
      return;
    }

    const actionsEl = contentEl.createDiv({ cls: 'gmail-launcher-actions' });
    accounts.forEach((account, index) => {
      const button = actionsEl.createEl('button', {
        cls: 'mod-cta gmail-launcher-button',
        text: account.name
      });
      button.createEl('span', {
        cls: 'gmail-launcher-meta',
        text: account.url
      });
      button.addEventListener('click', async () => {
        await this.plugin.openAccount(index);
      });
    });
  }
}

class GmailSidebarSettingTab extends PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display() {
    const { containerEl } = this;
    containerEl.empty();

    containerEl.createEl('h2', { text: 'Gmail Sidebar Launcher' });

    new Setting(containerEl)
      .setName('Launcher location')
      .setDesc('Where the Gmail launcher panel should open.')
      .addDropdown((dropdown) => {
        dropdown
          .addOption('left', 'Left sidebar')
          .addOption('right', 'Right sidebar')
          .setValue(this.plugin.settings.launcherIn)
          .onChange(async (value) => {
            this.plugin.settings.launcherIn = value;
            await this.plugin.saveSettings();
          });
      });

    new Setting(containerEl)
      .setName('Open target')
      .setDesc('Where Gmail should open inside Obsidian when launched.')
      .addDropdown((dropdown) => {
        dropdown
          .addOption('right', 'Right sidebar')
          .addOption('tab', 'Main workspace tab')
          .setValue(this.plugin.settings.openIn)
          .onChange(async (value) => {
            this.plugin.settings.openIn = value;
            await this.plugin.saveSettings();
          });
      });

    new Setting(containerEl)
      .setName('Gmail accounts')
      .setDesc('One account per line. Format: Name | URL. Example: Work | https://mail.google.com/mail/u/0/#inbox')
      .addTextArea((text) => {
        text
          .setPlaceholder('Primary | https://mail.google.com/mail/u/0/#inbox')
          .setValue(this.plugin.settings.accountsText)
          .onChange(async (value) => {
            this.plugin.settings.accountsText = value;
            await this.plugin.saveSettings();
            this.plugin.refreshLauncherViews();
          });
        text.inputEl.rows = 8;
        text.inputEl.cols = 60;
      });
  }
}

module.exports = class GmailSidebarLauncherPlugin extends Plugin {
  async onload() {
    await this.loadSettings();

    this.registerView(
      VIEW_TYPE_GMAIL_LAUNCHER,
      (leaf) => new GmailLauncherView(leaf, this)
    );

    this.addRibbonIcon('mail', 'Open Gmail', async () => {
      await this.openAccount(0);
    });

    this.addCommand({
      id: 'open-gmail-launcher',
      name: 'Open Gmail launcher',
      callback: async () => {
        await this.activateLauncherView();
      }
    });

    this.addCommand({
      id: 'open-primary-gmail-account',
      name: 'Open primary Gmail account',
      callback: async () => {
        await this.openAccount(0);
      }
    });

    this.addSettingTab(new GmailSidebarSettingTab(this.app, this));
  }

  async onunload() {
    this.app.workspace.detachLeavesOfType(VIEW_TYPE_GMAIL_LAUNCHER);
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }

  getAccounts() {
    return parseAccounts(this.settings.accountsText);
  }

  getTargetLeaf() {
    if (this.settings.openIn === 'tab') {
      return this.app.workspace.getLeaf(true);
    }
    return this.app.workspace.getRightLeaf(false);
  }

  async openAccount(index) {
    const accounts = this.getAccounts();
    const account = accounts[index];
    if (!account) {
      new Notice('No Gmail account configured for that slot.');
      return;
    }

    try {
      const leaf = this.getTargetLeaf();
      await leaf.setViewState({
        type: 'webviewer',
        active: true,
        state: {
          url: account.url,
          title: account.name,
          mode: 'webview'
        }
      });
      this.app.workspace.revealLeaf(leaf);
      new Notice(`Opened ${account.name} in Obsidian`);
    } catch (error) {
      console.error('Failed to open Gmail in Obsidian', error);
      new Notice(`Failed to open ${account.name}`);
    }
  }

  async activateLauncherView() {
    const leaf = this.settings.launcherIn === 'right'
      ? this.app.workspace.getRightLeaf(false)
      : this.app.workspace.getLeftLeaf(false);
    await leaf.setViewState({ type: VIEW_TYPE_GMAIL_LAUNCHER, active: true });
    this.app.workspace.revealLeaf(leaf);
  }

  refreshLauncherViews() {
    this.app.workspace.getLeavesOfType(VIEW_TYPE_GMAIL_LAUNCHER).forEach((leaf) => {
      if (leaf.view && typeof leaf.view.render === 'function') {
        leaf.view.render();
      }
    });
  }
};

import * as vscode from 'vscode';
import { OpenMetadataClient, TableMetadata } from './openmetadataClient';

export class TableHoverProvider implements vscode.HoverProvider {
    constructor(private client: OpenMetadataClient) {}

    async provideHover(document: vscode.TextDocument, position: vscode.Position): Promise<vscode.Hover | null> {
        const wordRange = document.getWordRangeAtPosition(position);
        if (!wordRange) return null;
        const word = document.getText(wordRange);
        if (!/^[a-z_][a-z0-9_]*$/i.test(word)) return null;

        const table = await this.client.getTable(word);
        if (!table) return null;

        const markdown = new vscode.MarkdownString();
        markdown.appendMarkdown(`### 📊 **${table.name}**\n\n`);
        if (table.description) markdown.appendMarkdown(`*${table.description}*\n\n`);
        markdown.appendMarkdown(`**Owner:** ${table.owner || 'Unknown'}\n`);
        markdown.appendMarkdown(`**Tags:** ${table.tags.map(t => `\`${t}\``).join(' ')}\n\n`);
        markdown.appendMarkdown(`#### Columns\n`);
        markdown.appendMarkdown(`| Column | Type | Description |\n`);
        markdown.appendMarkdown(`|--------|------|-------------|\n`);
        for (const col of table.columns.slice(0, 10)) {
            markdown.appendMarkdown(`| \`${col.name}\` | ${col.dataType} | ${col.description || '-'} |\n`);
        }
        if (table.downstreamCount && table.downstreamCount > 0) {
            markdown.appendMarkdown(`\n⚠️ **${table.downstreamCount} downstream dependencies** – changes may break dashboards.\n`);
        }
        markdown.supportHtml = true;
        return new vscode.Hover(markdown);
    }
}
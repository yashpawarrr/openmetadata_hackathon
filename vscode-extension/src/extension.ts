import * as vscode from 'vscode';
import { OpenMetadataClient } from './openmetadataClient';
import { TableHoverProvider } from './hoverProvider';
import { OptimizationCoach } from './inlineCoach';

export function activate(context: vscode.ExtensionContext) {
    const client = new OpenMetadataClient();
    const hoverProvider = new TableHoverProvider(client);
    const coach = new OptimizationCoach(client);

    context.subscriptions.push(
        vscode.languages.registerHoverProvider(['sql', 'jinja-sql'], hoverProvider)
    );

    // Run coach on document open and save
    const runCoach = () => {
        const editor = vscode.window.activeTextEditor;
        if (editor && editor.document.languageId === 'sql') {
            coach.analyzeDocument(editor.document);
        }
    };
    context.subscriptions.push(vscode.workspace.onDidOpenTextDocument(runCoach));
    context.subscriptions.push(vscode.workspace.onDidSaveTextDocument(runCoach));
    runCoach();

    // Natural language search command
    const searchCmd = vscode.commands.registerCommand('openmetadata.search', async () => {
        const query = await vscode.window.showInputBox({ prompt: 'Ask about your data...' });
        if (query) {
            const result = await client.naturalLanguageSearch(query);
            vscode.window.showInformationMessage(result);
        }
    });
    context.subscriptions.push(searchCmd);
}

export function deactivate() {}
import * as vscode from 'vscode';
import { OpenMetadataClient } from './openmetadataClient';

export class OptimizationCoach {
    constructor(private client: OpenMetadataClient) {}

    async analyzeDocument(document: vscode.TextDocument) {
        const text = document.getText();
        // Simple regex to find SELECT * FROM table
        const selectStarPattern = /SELECT\s+\*\s+FROM\s+(\w+)/gi;
        let match;
        while ((match = selectStarPattern.exec(text)) !== null) {
            const tableName = match[1];
            const table = await this.client.getTable(tableName);
            if (table && table.size && table.size > 1000 && !text.toLowerCase().includes('where')) {
                const range = document.getWordRangeAtPosition(document.positionAt(match.index));
                if (range) {
                    const diagnostic = {
                        message: `⚠️ Table ${tableName} is large (${table.size} rows) and has no WHERE clause. This may cause a full table scan. Consider adding a filter.`,
                        range: range,
                        severity: vscode.DiagnosticSeverity.Warning,
                        source: 'OpenMetadata Coach'
                    };
                    // Push diagnostic
                }
            }
            // Check partition usage
            if (table && table.partitions && table.partitions.length > 0 && !text.toLowerCase().includes(table.partitions[0].toLowerCase())) {
                const diagnostic = {
                    message: `💡 Table ${tableName} is partitioned by ${table.partitions[0]}. Add a filter on this column for better performance.`,
                    range: range,
                    severity: vscode.DiagnosticSeverity.Information,
                    source: 'OpenMetadata Coach'
                };
            }
        }
    }
}
import axios from 'axios';
import * as vscode from 'vscode';

export interface TableMetadata {
    name: string;
    description?: string;
    owner?: string;
    columns: Column[];
    size?: number;
    partitions?: string[];
    qualityScore?: number;
    downstreamCount?: number;
    tags: string[];
}

export interface Column {
    name: string;
    dataType: string;
    description?: string;
    nullable: boolean;
    constraints?: string[];
}

export class OpenMetadataClient {
    private host: string;
    private token: string;

    constructor() {
        const config = vscode.workspace.getConfiguration('openmetadata');
        this.host = config.get<string>('host', 'http://localhost:8585');
        this.token = config.get<string>('token', '');
    }

    private async request<T>(path: string): Promise<T | null> {
        try {
            const response = await axios.get(`${this.host}/api/v1${path}`, {
                headers: { Authorization: `Bearer ${this.token}` }
            });
            return response.data;
        } catch (error) {
            console.error(`OpenMetadata API error: ${error}`);
            return null;
        }
    }

    async getTable(fqn: string): Promise<TableMetadata | null> {
        const data = await this.request<{ name: string; description?: string; owner?: { name: string }; columns: any[]; tableSize?: number; tablePartition?: string; tags?: any[] }>(`/tables/name/${fqn}`);
        if (!data) return null;
        return {
            name: data.name,
            description: data.description,
            owner: data.owner?.name,
            columns: data.columns.map(col => ({
                name: col.name,
                dataType: col.dataType,
                description: col.description,
                nullable: col.nullable,
                constraints: col.constraints || []
            })),
            size: data.tableSize,
            partitions: data.tablePartition ? [data.tablePartition] : [],
            tags: (data.tags || []).map(t => t.tagFQN),
            downstreamCount: undefined
        };
    }

    async getDownstreamCount(fqn: string): Promise<number> {
        const lineage = await this.request<{ downstreamEdges: any[] }>(`/lineage/table/name/${fqn}?downstreamDepth=1`);
        return lineage?.downstreamEdges?.length || 0;
    }

    async naturalLanguageSearch(query: string): Promise<string> {
        // Call your AI search endpoint (could be a separate microservice or OpenMetadata's search)
        const results = await this.request<any[]>(`/search/query?q=${encodeURIComponent(query)}`);
        if (!results || results.length === 0) return "No results found.";
        return results.map(r => `- ${r.name}: ${r.description || 'No description'}`).join('\n');
    }
}
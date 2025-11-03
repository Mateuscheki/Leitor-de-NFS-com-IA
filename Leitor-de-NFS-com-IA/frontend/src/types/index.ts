export type NotaFiscalStatus = 'PENDENTE' | 'PROCESSADO' | 'ERRO';

export interface INotaFiscal {
    id: number;
    nome_prestador: string | null;
    cnpj_prestador: string | null;
    valor_total: number | null;
    codigo_servico: string | null;
    status_processamento: NotaFiscalStatus;
    tem_retencao_impostos: boolean;
}

export interface IPaginatedNfResponse {
    total: number;
    items: INotaFiscal[];
}
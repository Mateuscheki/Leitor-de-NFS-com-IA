import React, { useState } from 'react';
import { Box, Chip, Typography } from '@mui/material';
import { DataGrid, GridColDef, GridRenderCellParams, GridPaginationModel } from '@mui/x-data-grid';
// CORREÇÃO 1: Importar o 'keepPreviousData'
import { useQuery, keepPreviousData } from '@tanstack/react-query';
import { getNotasFiscais } from '../api/apiService';
import { INotaFiscal, NotaFiscalStatus } from '../types';

// Função helper para formatar o status
const renderStatus = (params: GridRenderCellParams<any, NotaFiscalStatus>) => {
    const status = params.value;
    let color: 'default' | 'warning' | 'success' | 'error' = 'default';

    switch (status) {
        case 'PENDENTE':
            color = 'warning';
            break;
        case 'PROCESSADO':
            color = 'success';
            break;
        case 'ERRO':
            color = 'error';
            break;
    }
    return <Chip label={status} color={color} size="small" />;
};

// Definição das colunas
const columns: GridColDef<INotaFiscal>[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'nome_prestador', headerName: 'Prestador', flex: 1.5, minWidth: 200 },
    { field: 'cnpj_prestador', headerName: 'CNPJ', flex: 1, minWidth: 150 },
    {
        field: 'valor_total',
        headerName: 'Valor (R$)',
        type: 'number',
        flex: 0.5,
        minWidth: 120,
    },
    { field: 'codigo_servico', headerName: 'Cód. Serviço', flex: 0.5, minWidth: 100 },
    {
        field: 'tem_retencao_impostos',
        headerName: 'Retenção',
        type: 'boolean',
        flex: 0.5,
        minWidth: 100,
    },
    {
        field: 'status_processamento',
        headerName: 'Status',
        flex: 0.7,
        minWidth: 130,
        renderCell: renderStatus,
    },
];

export const NotaFiscalTable: React.FC = () => {
    // Estado da paginação (controlado pelo MUI DataGrid)
    const [paginationModel, setPaginationModel] = useState({
        page: 0,
        pageSize: 10,
    });

    // useQuery (React Query) para buscar os dados
    const { data, isLoading, isError, error } = useQuery({
        queryKey: ['notasFiscais', paginationModel.page, paginationModel.pageSize],
        queryFn: () => getNotasFiscais(paginationModel.page, paginationModel.pageSize),
        
        // CORREÇÃO 2: Mudar de 'keepPreviousData: true' para 'placeholderData: keepPreviousData'
        placeholderData: keepPreviousData, // Mantém dados anteriores enquanto busca novos

        refetchInterval: 5000, // Opcional: Polling para atualizar status PENDENTE
    });

    if (isError) {
        return <Typography color="error">Erro ao buscar dados: {String(error)}</Typography>;
    }

    return (
        <Box sx={{ height: 600, width: '100%' }}>
            <DataGrid
                rows={data?.items || []}
                columns={columns}
                rowCount={data?.total || 0}
                loading={isLoading}
                paginationMode="server" // Paginação no lado do servidor
                paginationModel={paginationModel}
                onPaginationModelChange={setPaginationModel}
                pageSizeOptions={[5, 10, 20]}
                disableRowSelectionOnClick
            />
        </Box>
    );
};
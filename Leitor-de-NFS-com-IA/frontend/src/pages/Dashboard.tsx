import React from 'react';
import { Box, Paper } from '@mui/material';
import { FileUpload } from '../components/FileUpload';
import { NotaFiscalTable } from '../components/NotaFiscalTable';
import { useQueryClient } from '@tanstack/react-query';

const Dashboard: React.FC = () => {
    const queryClient = useQueryClient();

    // Esta função será chamada pelo FileUpload após um upload bem-sucedido
    const handleUploadSuccess = () => {
        // Invalida a query 'notasFiscais', forçando o React Query
        // a buscar os dados novamente (e exibir o novo item PENDENTE)
        queryClient.invalidateQueries({ queryKey: ['notasFiscais'] });
    };

    return (
        <Box>
            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
                <FileUpload onUploadSuccess={handleUploadSuccess} />
            </Paper>
            <Paper elevation={3} sx={{ p: 3 }}>
                <NotaFiscalTable />
            </Paper>
        </Box>
    );
};

export default Dashboard;
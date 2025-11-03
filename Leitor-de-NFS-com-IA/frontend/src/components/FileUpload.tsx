import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Box, Typography, CircularProgress, Alert } from '@mui/material';
import { UploadFile } from '@mui/icons-material';
import { useMutation } from '@tanstack/react-query';
import { uploadNotaFiscal } from '../api/apiService';

interface FileUploadProps {
    onUploadSuccess: () => void; // Callback para atualizar a tabela
}

export const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
    const [error, setError] = useState<string | null>(null);

    // useMutation (React Query) para lidar com o upload
    const mutation = useMutation({
        mutationFn: uploadNotaFiscal,
        onSuccess: (data) => {
            console.log('Upload bem-sucedido:', data.message);
            onUploadSuccess(); // Chama o callback
            setError(null);
        },
        onError: (err: any) => {
            console.error('Erro no upload:', err);
            setError(err.response?.data?.detail || 'Erro desconhecido no upload.');
        },
    });

    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles.length > 0) {
            mutation.mutate(acceptedFiles[0]); // Inicia o upload
        }
    }, [mutation]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
            'image/png': ['.png'],
            'image/jpeg': ['.jpg', '.jpeg'],
        },
        multiple: false,
    });

    return (
        <Box
            {...getRootProps()}
            sx={{
                border: '2px dashed',
                borderColor: isDragActive ? 'primary.main' : 'grey.400',
                borderRadius: 2,
                p: 4,
                textAlign: 'center',
                cursor: 'pointer',
                backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
                mb: 4,
            }}
        >
            <input {...getInputProps()} />
            {mutation.isPending ? ( // 'isPending' é o novo 'isLoading'
                <Box>
                    <CircularProgress />
                    <Typography>Enviando...</Typography>
                </Box>
            ) : (
                <Box>
                    <UploadFile sx={{ fontSize: 48, color: 'grey.500' }} />
                    <Typography>
                        {isDragActive
                            ? 'Solte o arquivo aqui...'
                            : 'Arraste e solte a Nota Fiscal aqui, ou clique para selecionar (PDF, PNG, JPG)'}
                    </Typography>
                </Box>
            )}
            {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
            {mutation.isSuccess && <Alert severity="success" sx={{ mt: 2 }}>Upload recebido! O processamento foi iniciado.</Alert>}
        </Box>
    );
};
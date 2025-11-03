import axios from 'axios';
import { IPaginatedNfResponse } from '../types';

// URL base da nossa API (definida pelo Docker Compose ou Nginx)
const API_URL = '/api/v1';

const apiClient = axios.create({
    baseURL: API_URL,
});

/**
 * Busca a lista paginada de notas fiscais.
 */
export const getNotasFiscais = async (page: number = 0, pageSize: number = 10): Promise<IPaginatedNfResponse> => {
    const response = await apiClient.get('/notas/', {
        params: {
            skip: page * pageSize,
            limit: pageSize,
        },
    });
    return response.data;
};

/**
 * Faz o upload do arquivo de nota fiscal.
 */
export const uploadNotaFiscal = async (file: File): Promise<{ message: string; nota_id: number }> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post('/notas/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};
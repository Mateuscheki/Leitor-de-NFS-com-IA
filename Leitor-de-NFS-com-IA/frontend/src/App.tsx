import React from 'react';
import { CssBaseline, ThemeProvider, createTheme, Container, Typography } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Dashboard from './pages/Dashboard';

// Configura o cliente do React Query
const queryClient = new QueryClient();

// Tema básico do MUI
const theme = createTheme({
    palette: {
        mode: 'light', // ou 'dark'
        primary: {
            main: '#1976d2',
        },
    },
});

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <ThemeProvider theme={theme}>
                <CssBaseline /> {/* Reseta o CSS padrão do navegador */}
                <Container maxWidth="lg">
                    <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mt: 4, mb: 4 }}>
                        NF-Extractor 🧾
                    </Typography>
                    <Dashboard />
                </Container>
            </ThemeProvider>
        </QueryClientProvider>
    );
}

export default App;
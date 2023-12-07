import React, { createContext, useContext } from 'react';
import axios from 'axios';

const SessionContext = createContext();

export const useSession = () => {
    return useContext(SessionContext);
};

// Create a single Axios instance for the session
const session = axios.create({
    baseURL: 'http://localhost:8000/api/',
    withCredentials: true, // Enable cookies (for session management)
});

export const SessionProvider = ({ children }) => {
    session.get('csrf-token')
        .then(response => {
            const csrfToken = response.data.csrfToken;
            session.defaults.headers.common['X-CSRFToken'] = csrfToken
        })
        .catch(error => console.error('Error fetching CSRF token:', error))
    return (
        <SessionContext.Provider value={{ session }}>
            {children}
        </SessionContext.Provider>
    );
};

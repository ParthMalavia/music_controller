import './App.css';
import RoutesPage from './components/RoutesPage';
import { SessionProvider } from './components/SessionContext';


function App() {
  return (
    <div className='center'>
      <SessionProvider>
        <RoutesPage />
      </SessionProvider>
    </div>
  );
}

export default App;

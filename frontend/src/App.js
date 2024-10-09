import logo from './logo.svg';
import './App.css';
import Greet from './components/Nav_bar'

function App() {
  return (
    <div className="App">
      <Greet/>

      <div style={{ paddingTop: '60px', paddingBottom: '60px' }}>
        Your main content goes here
        <h1>Main Content Here</h1>
      </div>

    </div>
  );
}

export default App;

import React from 'react';
import logo from './logo.svg';
import './App.css';
import NavBar from './NavBar';

const links = [{label: "Main", link: "http://localhost:3000/"}, {label: "Dogs", link: "http://localhost:3000/dogs"}]

function App() {
  return (
    <div className="App">
      <NavBar links={links} currIndex={1} />
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;

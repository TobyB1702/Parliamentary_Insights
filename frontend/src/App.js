import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputValue, setInputValue] = useState('');
  const [entitySummary, setEntitySummary] = useState(''); // New state variable for entity summary

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleButtonClick = async () => {
    console.log(inputValue);
    try {
      const response = await fetch(`http://localhost:8000/query_parliamentary_data/${inputValue}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setEntitySummary(data.entity_response.entity_summary_answer); // Set the returned entity summary directly
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
      setEntitySummary('Error fetching data');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Parliamentary Insights</h1>
      </header>
      <div className="App-body">
        <div className="App-inputContainer">
          <input
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Enter Entity"
            className="App-input"
          />
          <button onClick={handleButtonClick} className="App-button">
            Submit
          </button>
        </div>
        {entitySummary && (
          <div className="App-entitySummary">
            <textarea
              value={entitySummary}
              readOnly
              className="App-textarea"
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
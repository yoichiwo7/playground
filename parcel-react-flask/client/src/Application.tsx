import * as React from 'react';
import axios from 'axios'

class Application extends React.Component {

  onClick = (event) => {
    console.log("clicked!!")
    const job = axios.get('hello')
    job.then((response) => {
      console.log(response.status + ":" + response.data)
    })
  }
  render() {
    return (
      <div>
        <h1>Hello World!!</h1>
        <button onClick={this.onClick}>Press</button>
        <ul>
          <li>123</li>
          <li>124</li>
          <li>125</li>
        </ul>
      </div>
    );
  }  
}

export default Application;

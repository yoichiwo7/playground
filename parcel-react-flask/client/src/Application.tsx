import * as React from 'react';
import axios from 'axios'

class Application extends React.Component {

  onGET = (event) => {
    console.log("GET clicked!!")
    const job = axios.get('hello')
    job.then((response) => {
      console.log(response.status + ":" + response.data)
    })
  }

  onPOST = (event) => {
    console.log("POST clicked!!")
    const job = axios.post('echo', {
      firstName: 'Taro',
      lastName: 'Yamada',
      age: 20
    })
    job.then((response) => {
      console.log(response.status + ":" + JSON.stringify(response.data))
    })
  }

  render() {
    return (
      <div>
        <h1>Send request to the server:</h1>
        <div>
          <button onClick={this.onGET}>GET</button>
        </div>
        <div>
          <button onClick={this.onPOST}>POST</button>
        </div>
      </div>
    );
  }  
}

export default Application;

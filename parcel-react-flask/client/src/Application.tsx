import * as React from 'react';
import axios from 'axios'
import Chart = require('chart.js');

class Application extends React.Component {

  onGET = async (event) => {
    console.log("GET clicked!!")
    const response = await axios.get('hello')
    console.log(response.status + ":" + response.data)
  }

  onPOST = async (event) => {
    console.log("POST clicked!!")
    const response = await axios.post('echo', {
      firstName: 'Taro',
      lastName: 'Yamada',
      age: 20
    })
    console.log(response.status + ":" + JSON.stringify(response.data))
  }

  onChart = async (event) => {
    console.log("Chart clicked!!")
    let dataset = [0, 10, 5, 2, 20, 30, 45] //default
    const response = await axios.get('dataset')
    dataset = response.data

    //TODO:
    const ctx = (this.refs.canvas as HTMLCanvasElement).getContext('2d')
    const chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: ["January", "February", "March", "April", "May", "June", "July"],
            datasets: [{
                label: "My First dataset",
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: dataset
            }]
        },

        // Configuration options go here
        options: {}
    });
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

        <h1>Chartjs example:</h1>
        <div>
          <button onClick={this.onChart}>Show Chart</button>
        </div>
        <div>
          <canvas ref="canvas"></canvas>
        </div>
      </div>
    );
  }  
}

export default Application;

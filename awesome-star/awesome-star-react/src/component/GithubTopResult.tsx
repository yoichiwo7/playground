import * as React from "react";
import { GithubRepo } from "./GithubInput";
import { Bar } from "react-chartjs-2";
import Griddle, { RowDefinition, ColumnDefinition } from "griddle-react";

interface Props {
  repos: GithubRepo[];
  topN: number;
}

class GithubTopResult extends React.PureComponent<Props> {
  chartOptions = {
    scales: {
      yAxes: [{ ticks: { beginAtZero: true } }]
    }
  };

  constructor(props: Props) {
    super(props);
  }

  getChartData = () => {
    const topRepos = this.props.repos.slice(0, this.props.topN);
    return {
      labels: topRepos.map(e => e.repo),
      datasets: [
        {
          data: topRepos.map(e => e.star),
          label: "Star",
          borderWidth: 4,
          borderColor: "rgba(132, 99, 255, 1.0)",
          backgroundColor: "rgba(132, 99, 255, 0.4)"
        }
      ]
    };
  };

  public render() {
    const topRepos = this.props.repos.slice(0, this.props.topN);
    const data = topRepos.map((elem, idx) => {
      return {
        rank: idx + 1,
        name: elem.repo,
        star: elem.star,
        license: elem.license,
        updated: elem.lastUpdated
      };
    });

    return (
      <div>
        {this.getTableJsx(data)}
        {this.getChartJsx()}
      </div>
    );
  }

  private getTableJsx = (data: object[]): React.ReactNode => {
    if (this.props.repos.length <= 0) {
      return;
    }
    return (
      <div>
        <h2>Top {this.props.topN} List</h2>
        <Griddle data={data}>
          <RowDefinition>
            <ColumnDefinition id="rank" />
            <ColumnDefinition id="name" />
            <ColumnDefinition id="star" />
            <ColumnDefinition id="license" />
            <ColumnDefinition id="updated" />
          </RowDefinition>
        </Griddle>
      </div>
    );
  };

  private getChartJsx = (): React.ReactNode => {
    if (this.props.repos.length <= 0) {
      return;
    }
    return (
      <div>
        <h2>Top {this.props.topN} Chart</h2>
        <Bar data={this.getChartData()} options={this.chartOptions} />
      </div>
    );
  };
}

export default GithubTopResult;

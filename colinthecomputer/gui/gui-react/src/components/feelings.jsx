import React, { Component } from "react";
import Loading from "./loading";

class Feelings extends Component {
  state = { loaded: null, feelings: null };
  render() {
    if (!this.state.loaded) {
      return <Loading />;
    }
    var feelings = [];
    for (let i in Object.keys(this.state.feelings)) {
      let key = Object.keys(this.state.feelings)[i];
      let value = this.state.feelings[key];
      let icon = null;
      if (value >= 0.75) {
        icon = `/icons/${key}1.PNG`;
      } else if (value >= 0.25) {
        icon = `/icons/${key}0.5.PNG`;
      } else if (value >= 0) {
        icon = `/icons/${key}0.PNG`;
      } else if (value >= -0.25) {
        icon = `/icons/${key}-0.5.PNG`;
      } else {
        icon = `/icons/${key}-1.PNG`;
      }
      feelings.push(
        <img
          src={icon}
          title={key}
          alt={`${key}: ${value.toFixed(3)}`}
          width="35px"
        />
      );
    }

    return (
      <div
        class="jumbotron"
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          width: "60vh",
          height: "40vh",
        }}
      >
        <div class="text-center">
          <h5>Feelings</h5>
          {feelings}
        </div>
      </div>
    );
  }

  componentDidMount = () => {
    var user_id = this.props.user_id;
    var snapshot_id = this.props.snapshot_id;
    fetch(
      `${window.api_root}/users/${user_id}/snapshots/${snapshot_id}/feelings`,
      {
        method: "GET",
        mode: "cors",
        dataType: "json",
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response;
      })
      .then((response) => response.json())
      .then((data) => {
        this.setState({ loaded: true, feelings: data });
      })
      .catch((error) => {
        console.log(error); // todo
      });
  };
}

export default Feelings;

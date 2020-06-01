import React, { Component } from "react";
import Loading from "./loading";
import Pose from "./pose";
import Image from "./image";
import Feelings from "./feelings";
import ErrorPage from "./error";
import { Link } from "react-router-dom";
import _ from "lodash";

class SnapshotInfo extends Component {
  state = {
    error: null,
    isLoaded: false,
  };

  renderField(field, component) {
    if (!this.state.results.includes(field)) {
      return (
        <div
          class="m-2 container"
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div
            class="jumbotron"
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              width: "42vh",
              height: "40vh",
            }}
          >
            <p class="text-center">
              {" "}
              {`${field.replace("_", " ")} is not available`}{" "}
            </p>
          </div>
        </div>
      );
    }
    return (
      <div
        class="m-2 container"
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        {component}
      </div>
    );
  }

  renderNav(direction) {
    var snapshots = _.sortBy(this.state.snapshots, ["datetime"]);
    const isCurrent = (snapshot) => snapshot.datetime == this.state.datetime;
    var index = snapshots.findIndex(isCurrent);
    var toIndex, arrow;
    if (direction == "prev") {
      toIndex = index - 1;
      arrow = "/arrows/left.PNG";
    } else if (direction == "next") {
      toIndex = index + 1;
      arrow = "/arrows/right.PNG";
    }

    if (toIndex < 0 || toIndex >= snapshots.length) {
      return <a />;
    }

    return (
      <div
        class="container"
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Link
          to={{
            pathname: `${snapshots[toIndex].snapshot_id}`,
            state: {
              snapshots: snapshots,
              index: toIndex,
            },
          }}
        >
          <img src={arrow} alt={direction} title={direction} width="40px" />
        </Link>
      </div>
    );
  }

  renderDatetime(timestamp) {
    var date = new Date(timestamp);
    return <p>{`${date.toLocaleString()}`}</p>;
  }

  render() {
    if (this.state.error) {
      return <ErrorPage error={this.state.error} />;
    }
    if (!this.state.isLoaded) {
      return <Loading />;
    }

    return (
      <div>
        <nav
          class="navbar navbar-expand-lg navbar-light"
          style={{ backgroundColor: "#e6fff2" }}
        >
          <a class="navbar-brand" href="/">
            <img
              src="/icons/colin.PNG"
              width="40px"
              class="d-inline-block align-top"
              alt=""
            />
          </a>
          <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav mr-auto">
              <a
                class="nav-item nav-link"
                href={`/users/${this.state.user_id}/snapshots/`}
              >
                <img
                  src="/arrows/back.PNG"
                  width="40px"
                  class="d-inline-block align-top"
                  alt=""
                />
              </a>
            </div>
            <span class="navbar-text">
              {this.renderDatetime(this.state.datetime)}
            </span>
          </div>
        </nav>
        <div
          class="mt-3 container"
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div class="col">{this.renderNav("prev")}</div>
          <div class="col px-md-5">
            <div class="row">
              {this.renderField(
                "pose",
                <Pose
                  user_id={this.state.user_id}
                  snapshot_id={this.state.snapshot_id}
                />
              )}
            </div>
            <div class="row">
              {this.renderField(
                "feelings",
                <Feelings
                  user_id={this.state.user_id}
                  snapshot_id={this.state.snapshot_id}
                />
              )}
            </div>
          </div>
          <div class="col px-md-5">
            <div class="row">
              {this.renderField(
                "color_image",
                <Image
                  user_id={this.state.user_id}
                  snapshot_id={this.state.snapshot_id}
                  type="color_image"
                />
              )}
            </div>
            <div class="row">
              {this.renderField(
                "depth_image",
                <Image
                  user_id={this.state.user_id}
                  snapshot_id={this.state.snapshot_id}
                  type="depth_image"
                />
              )}
            </div>
          </div>
          <div class="col">
            <div
              class="container"
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              {this.renderNav("next")}
            </div>
          </div>
        </div>
      </div>
    );
  }

  fetch_results = (results) => {
    var fetched_results = {};
    for (var i = 0; i < results.length; i++) {
      fetched_results[results[i]] = this.fetch_result(results[i]);
    }
    return fetched_results;
  };

  componentDidMount = () => {
    var user_id = this.props.match.params.user_id;
    var snapshot_id = this.props.match.params.snapshot_id;
    fetch(`${window.api_root}/users/${user_id}/snapshots/${snapshot_id}`, {
      method: "GET",
      mode: "cors",
      dataType: "json",
    })
      .then((response) => {
        if (!response.ok) {
          this.setState({
            isLoaded: true,
            error: { status: response.status, text: response.statusText },
          });
          throw Error(response);
        }
        return response;
      })
      .then((response) => response.json())
      .then((data) => {
        this.state.user_id = user_id;
        this.state.snapshot_id = snapshot_id;
        this.setState({
          isLoaded: true,
          user_id: user_id,
          datetime: data.datetime,
          snapshot_id: snapshot_id,
          results: data.results,
        });
      })
      .then(() => {
        fetch(`${window.api_root}/users/${user_id}/snapshots`, {
          method: "GET",
          mode: "cors",
          dataType: "json",
        })
          .then((response) => response.json())
          .then((data) => {
            this.setState({
              snapshots: data,
            });
          });
      })
      .catch((error) => {
        // pass
      });
  };
}

export default SnapshotInfo;

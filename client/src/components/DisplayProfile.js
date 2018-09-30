import React, { Component } from 'react';

export class DisplayProfile extends Component {
  constructor(props) {
    super(props)
    this.state = {
      viewImage: false
    }
  }
  


  toggleViewImage = () => {
    this.setState ({
      viewImage: !this.state.viewImage
    })
  }

  render() {
    console.log(this);
    return (
      <div>
        {this.props.name}
        {this.props.age}
        <img src={this.props.image_url}></img>
    <button onClick={this.toggleViewImage}>View Picture</button>
    { this.state.viewImage ? <div><img src={this.props.image_url}/></div> : <div>Load image</div> } 
  </div>
    )
  }
}


import React, { Component } from 'react';
import { graphql } from 'react-apollo'; // what actually binds react to apollo
import { getProfilesQuery } from '../queries/queries'
import axios from 'axios'
import { FACE_API_KEY, FACE_LIST_URL, SERVER_URL} from '../constants'

class ListProfiles extends Component {
  constructor(props){
    super(props);
    this.state = {
      displayCount: 0,
      profiles: [],
      profilesNotShown: []
    }
  }

  addToFaceList = (imageUrl) => {
    let postOptions = {
      method: 'post',
      url: FACE_LIST_URL,
      headers: {'Ocp-Apim-Subscription-Key': FACE_API_KEY,
                "Content-Type": "application/json"},
      data: {"url": imageUrl}
    }

    console.log(postOptions);
    axios(postOptions,
    ).then(response =>{
      console.log(response)
      })
      .catch(error =>{
      console.log(error);
      })
  }

  deleteProfile = (id) => {
    let postOptions = {
      method: 'post',
      url: SERVER_URL + "/delete",
      headers: {
        id: id
      }
    }
    
    let newProfiles = this.state.profiles;
    let newProfilesNotShown = this.state.profilesNotShown;

    axios(postOptions)
    .then(response => {
      console.log(response)
      if(response.status === 200) {
        
        for(let i = 0; i < newProfiles.length; i++) {
          if(newProfiles[i].id == id) {
            newProfiles.splice(i, 1);
            break;
          }
        }

        for(let i=0; i < newProfilesNotShown.length; i++) {
          if(newProfilesNotShown[i].id == id) {
            newProfilesNotShown.splice(i, 1);
            break;
          }
        }

        this.setState({
          profiles: newProfiles,
          profilesNotShow: newProfilesNotShown,
          displayCount: this.state.displayCount - 1
        }) 
        console.log("200")
      }
    })
    .catch(error => {
      console.log(error)
    })
  }

  loadAll  = () =>{

    this.setState ({
      displayCount: 0,
      profilesNotShown: this.props.data.profiles
    })
  }

  loadMore  = () =>{
    console.log("load more")
    let newDisplayCount = this.state.displayCount;
    newDisplayCount += 10

    let newProfiles = this.state.profilesNotShown.slice(0, this.state.displayCount)

    this.setState({
      displayCount: newDisplayCount
    })

    this.setState ({
      profiles: newProfiles
    })
  }

  displayProfiles() {
    
    if(this.props.data.loading) {
      return <div>Loading profiles...</div>
    } else {
      return this.state.profiles.map(profile => {
        //console.log(profile)
        return profile.reason === 'passed' ? (
          <div >
            <div>----------------------------------------------------------------------------------------</div>
              {profile.name}
              {profile.age}
              <div></div>
              <img width='300px' src={profile.image_url}></img>
              <button onClick={()=>this.addToFaceList(profile.image_url)}>Add to Face List</button>
              <button onClick={() => this.deleteProfile(profile.id)}>Delete</button>
            <div>----------------------------------------------------------------------------------------</div>
          </div> 
        
        ) : <div><button onClick={() => this.deleteProfile(profile.id)}>Delete(didn't pass)</button></div>
      })
  }
}

  render() {
    return (
      <div>
        <button onClick={this.loadAll}>Load All</button>
        <button onClick={this.loadMore}>
        Load More
        </button>
        { this.displayProfiles() }
        <button onClick={this.loadMore}>
        Load More
        </button>
      </div>
    );
  }
}


// below we are taking the "getBooksQuery" query and binding it to the BookList component
// it stores the query information in the components props

export default graphql(getProfilesQuery)(ListProfiles);

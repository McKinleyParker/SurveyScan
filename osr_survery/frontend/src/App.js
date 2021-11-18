
import './App.css';
import PropertyList from './components/property_list.js'
import ScanUpload from './components/scan_upload';
import PostTest from './components/post_test';
import NearbyPropertyFinder from './components/geolocation'

const behind_firewall_logo = "https://pic.onlinewebfonts.com/svg/img_384132.png"
// const not_firewall_logo = "https://img.icons8.com/color/48/000000/placeholder-thumbnail-edifact.png" 

function App() {
  return (
    <div className="App">
      <header className="nav_bar">
        <img src={behind_firewall_logo} className="App-logo" alt="logo" />
        <p>
          PropertyScan
        </p>
      </header>
      <PropertyList />
      <ScanUpload />
      <PostTest />
      <NearbyPropertyFinder />
    </div>
  );
}

export default App;


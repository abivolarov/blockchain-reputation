pragma solidity >=0.4.21 <0.6.0;

/// @author Anton Bivolarov

/*
  Smart Contract to manage blockchain road event and reputation storage
*/
contract Transmission {

    // A structure to store the reported road events
    struct RoadEvent {
      bytes32 eventType;
      uint date;
      address submittedBy;
    }

    // A structure to store message credibility information
    struct MessageFeedback {
        bool isCredible;
        uint date;
        address submittedBy;
    }


    // A hashmap datastructure to save the feedback given by an account for another account
    mapping (address => mapping (address => MessageFeedback)) public messageFeedbacks;

    // A variable to store the total number of events
    uint totalNumberOfEvents = 0;

    // A variable to store the actual event number
    uint numberOfEvent = 1;

    // A hashmap datastructure to save all road events
    mapping (uint => RoadEvent) public latestEvents;

    // A hashmap to save the total number of feedbacks given for a single address
    mapping (address => uint) public totalCount;

    // A hashmap to store the total reputation sum of an address
    mapping (address => uint) public reputationSum;

    /*
      Smart contract events used to present the contract's functions 
    */
    event SubmitFeedback(address indexed _from, address indexed _to, uint indexed _date, bool _isCredible);
    event SubmitRoadEvent(address indexed _from, uint indexed _date, uint8 _mark);

    /*
      Smart contract function to submit a new event on the road
    */
    function submitRoadEvent(uint8 _mark) public {
        require(_mark > 0 && _mark <= 3);

        if (_mark == 1) {
            latestEvents[numberOfEvent].eventType = "Traffic Congestion";
        } else if (_mark == 2) {
            latestEvents[numberOfEvent].eventType = "Emergency ahead";
        } else {
            latestEvents[numberOfEvent].eventType = "Road Closed";
        }

        latestEvents[numberOfEvent].date = now;

        latestEvents[numberOfEvent].submittedBy = msg.sender;

        totalNumberOfEvents++;
        numberOfEvent++;

        emit SubmitRoadEvent(msg.sender, now, _mark);
    }

    /*
      A method to submit a feedback about the credibility of a message
    */
    function submitFeedback(address _account, bool _isCredible) public {
        require(_account != address(0));
        require(_account != msg.sender);

        messageFeedbacks[_account][msg.sender].isCredible = _isCredible;

        messageFeedbacks[_account][msg.sender].date = now;

        messageFeedbacks[_account][msg.sender].submittedBy = msg.sender;


        if(_isCredible == true) {
          reputationSum[_account] += 5;

        } else {
          reputationSum[_account] += 1;
        }

        totalCount[_account]++;

        emit SubmitFeedback(msg.sender, _account, now, _isCredible);
    }

    /*
      A function to retrieve the reputation stored on the blockchain for a given account
    */
    function getReputation(address _account) view public returns (uint) {
      return (reputationSum[_account] / totalCount[_account]);
    }

    /*
      A function to retrieve the latest event submitted
    */
    function getLatestEventByIndex(uint index) view public returns (bytes32) {
        return latestEvents[index].eventType;
    }

    /*
      Function to retrieve the address of the account which has submitted the latest event
    */
    function getTheAddressOfTheLatestEvent(uint index) view public returns (address) {
        return latestEvents[index].submittedBy;
    }

    /*
      Function which returns the total number of events on the blockchain
    */
    function getNumberOfEvents() view public returns (uint) {
      return totalNumberOfEvents;
    }

}

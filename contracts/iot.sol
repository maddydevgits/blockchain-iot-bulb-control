pragma solidity 0.5.16;

contract iot {
	uint internal bulbState;
	address owner;

	constructor() public {
		owner=msg.sender;	
	}

	modifier onlyOwner {
		require(owner==msg.sender);
		_;
	}

	function controlBulb(uint s) public onlyOwner returns(uint){
		bulbState=s;
		return(bulbState);
	}
	
	function viewBulb() public view onlyOwner returns(uint) {
		return(bulbState);
	}
}

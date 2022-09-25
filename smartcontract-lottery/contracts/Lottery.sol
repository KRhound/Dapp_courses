// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract Lottery {
    address payable[] public players;
    uint256 public usdEntryFee;

    constructor() {
        usdEntryFee = 50 * (10**18);
    }

    function enter() public {
        // $50 minimum
        players.push(msg.sender);
    }

    function getEntanceFee() public {
        //
    }

    function startLottery() public {}

    function endLottery() public {}
}

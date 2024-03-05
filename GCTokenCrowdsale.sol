/*
GC-Token Crowdsale
*/

pragma solidity ^0.5.5;

import "./GCTokenMintable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";

contract GC_TokenCrowdsale is Crowdsale, MintedCrowdsale {
    constructor(
        uint256 rate,
        address payable wallet,
        GC_Token token
    )
      Crowdsale(rate, wallet, token)
      public
    {
        // constructor can stay empty
    }
}

contract GC_TokenCrowdsaleDeployer {
    address public gc_token_address;
    address public gc_crowdsale_address;

    constructor(
        string memory name,
        string memory symbol,
        address payable wallet
    )
    public
    {
        GC_Token token = new GC_Token(name, symbol, 0);
        gc_token_address = address(token);

        GC_TokenCrowdsale gc_crowdsale =
            new GC_TokenCrowdsale(1, wallet, token);
        gc_crowdsale_address = address(gc_crowdsale);

        token.addMinter(gc_crowdsale_address);
        token.renounceMinter();
    }
}

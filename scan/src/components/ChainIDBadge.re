module Styles = {
  open Css;

  let version =
    style([
      display(`flex),
      borderRadius(`px(10)),
      backgroundColor(Colors.blue1),
      padding2(~v=`pxFloat(5.), ~h=`px(8)),
      justifyContent(`center),
      minWidth(`px(120)),
      alignItems(`center),
      marginLeft(Spacing.xs),
      marginTop(`px(1)),
      position(`relative),
      cursor(`pointer),
      Media.mobile([minWidth(`px(160)), zIndex(4)]),
    ]);

  let versionLoading =
    style([
      display(`flex),
      borderRadius(`px(10)),
      backgroundColor(Colors.blue1),
      overflow(`hidden),
      height(`px(16)),
      width(`px(120)),
      justifyContent(`center),
      alignItems(`center),
      marginLeft(Spacing.xs),
      marginTop(`px(1)),
      Media.mobile([height(`px(25)), width(`px(160))]),
    ]);

  let downIcon = show =>
    style([
      width(`px(6)),
      marginTop(`px(1)),
      transform(`rotate(`deg(show ? 180. : 0.))),
      Media.mobile([width(`px(8)), height(`px(6))]),
    ]);

  let dropdown = show =>
    style([
      display(`flex),
      borderRadius(`px(10)),
      flexDirection(`column),
      justifyContent(`center),
      position(`absolute),
      width(`percent(100.)),
      alignItems(`center),
      backgroundColor(Colors.blue1),
      transition(~duration=200, "all"),
      top(`px(25)),
      height(`auto),
      padding4(~top=`pxFloat(4.), ~bottom=`zero, ~left=`px(8), ~right=`px(8)),
      opacity(show ? 1. : 0.),
      pointerEvents(show ? `auto : `none),
      Media.mobile([top(`px(35))]),
    ]);

  let link = style([textDecoration(`none)]);
};

type chainID =
  | WenchangTestnet
  | WenchangMainnet
  | GuanYuDevnet
  | GuanYuTestnet
  | Unknown;

let parseChainID =
  fun
  | "band-wenchang-testnet2" => WenchangTestnet
  | "band-wenchang-mainnet" => WenchangMainnet
  | "band-guanyu-devnet5"
  | "band-guanyu-devnet6"
  | "band-guanyu-devnet7"
  | "band-guanyu-devnet8"
  | "bandchain" => GuanYuDevnet
  | "band-guanyu-testnet1"
  | "band-guanyu-testnet2" => GuanYuTestnet
  | _ => Unknown;

let getLink =
  fun
  | WenchangTestnet => "https://wenchang-testnet.cosmoscan.io/"
  | WenchangMainnet => "https://cosmoscan.io/"
  | GuanYuDevnet => "https://guanyu-devnet.cosmoscan.io/"
  | GuanYuTestnet
  | Unknown => "";

let getName =
  fun
  | WenchangTestnet => "wenchang-testnet"
  | WenchangMainnet => "wenchang-mainnet"
  | GuanYuDevnet => "guanyu-devnet"
  | GuanYuTestnet => "guanyu-testnet"
  | Unknown => "unknown";

[@react.component]
let make = () =>
  {
    let isMobile = Media.isMobile();
    let (show, setShow) = React.useState(_ => false);
    let trackingSub = TrackingSub.use();
    let%Sub tracking = trackingSub;
    let currentChainID = tracking.chainID->parseChainID;

    <div
      className=Styles.version
      onClick={event => {
        setShow(oldVal => !oldVal);
        ReactEvent.Mouse.stopPropagation(event);
      }}>
      <Text
        value={currentChainID->getName}
        size={isMobile ? Text.Md : Text.Sm}
        color=Colors.blue6
        nowrap=true
        weight=Text.Semibold
        spacing={Text.Em(0.03)}
      />
      <HSpacing size=Spacing.sm />
      <img src=Images.triangleDown className={Styles.downIcon(show)} />
      <div className={Styles.dropdown(show)}>
        {[|WenchangTestnet, WenchangMainnet, GuanYuDevnet|]
         ->Belt.Array.keep(chainID => chainID != currentChainID)
         ->Belt.Array.map(chainID => {
             let name = chainID->getName;
             <a
               href={getLink(chainID)}
               key=name
               className=Styles.link
               target="_blank"
               rel="noopener">
               <Text
                 value=name
                 size={isMobile ? Text.Md : Text.Sm}
                 color=Colors.blue6
                 nowrap=true
                 weight=Text.Semibold
                 spacing={Text.Em(0.03)}
               />
               <VSpacing size={`px(8)} />
             </a>;
           })
         ->React.array}
      </div>
    </div>
    |> Sub.resolve;
  }
  |> Sub.default(
       _,
       <div className=Styles.versionLoading>
         {Media.isMobile()
            ? <LoadingCensorBar
                width=160
                height=25
                colorBase=Colors.blue1
                colorLighter=Colors.white
              />
            : <LoadingCensorBar
                width=120
                height=16
                colorBase=Colors.blue1
                colorLighter=Colors.white
              />}
       </div>,
     );

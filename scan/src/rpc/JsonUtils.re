module Decode = {
  include Json.Decode;
  let intstr = string |> map(int_of_string);
  let uamount = string |> map(Int64.of_string);
  let moment = string |> map(MomentRe.moment);
  let floatstr = string |> map(float_of_string);
};

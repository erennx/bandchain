use owasm::ext::ethgasstation::gas_price;
use owasm::ext::utils::date;
use owasm::{decl_data, decl_params, decl_result};

decl_params! {
    pub struct Parameter {
        pub gas_option: String,
    }
}

decl_data! {
    pub struct Data {
        pub gas_price: f32 = |params: &Parameter| gas_price::Price::new(&params.gas_option),
        pub time_stamp: u64 = |_: &Parameter| date::Date::new(),
    }
}

decl_result! {
    pub struct Result {
        pub gas_price_in_gwei: u64,
        pub time_stamp: u64,
    }
}

pub fn execute(_params: Parameter, data: Vec<Data>) -> Result {
    let mut total_gas_price = 0.0;
    let mut time_stamp_acc: u64 = 0;
    for each in &data {
        total_gas_price += each.gas_price;
        time_stamp_acc += each.time_stamp;
    }
    let average_gas_price = total_gas_price / (data.len() as f32);
    let avg_time_stamp = time_stamp_acc / (data.len() as u64);
    Result { gas_price_in_gwei: (average_gas_price * 100.0) as u64, time_stamp: avg_time_stamp }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_execute() {
        let params = Parameter { gas_option: String::from("average") };
        let data1 = Data { gas_price: 13.0, time_stamp: 10 };
        let data2 = Data { gas_price: 7.0, time_stamp: 12 };
        assert_eq!(
            execute(params, vec![data1, data2]),
            Result { gas_price_in_gwei: 1000, time_stamp: 11 }
        );
    }

    #[test]
    fn test_call_real_gas_price() {
        let params = Parameter { gas_option: String::from("average") };
        let data = Data::build_from_local_env(&params).unwrap();
        println!(
            "Current Ethereum gas price with average option (times 100) is {:?}",
            execute(params, vec![data])
        );
    }
}

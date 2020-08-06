from ..bridge import BRIDGE
from ..utils import *
from tbears.libs.scoretest.score_test_case import ScoreTestCase
from iconservice.base.exception import IconScoreException


class TestBRIDGE(ScoreTestCase):

    def setUp(self):
        super().setUp()
        self.score = self.get_score_instance(
            BRIDGE,
            self.test_account1,
            on_install_params={'validators_bytes':  bytes.fromhex(
                "0000000300000040a54ffaa84c8f2f798782de8b962a84784e288487a747813a0857243a60e2ba331db530b76775beb0348c52bb8fc1fdac207525e5689caa01c0af8d2f8f371ec5000000000000006400000040724ae29cfeb7497051d09edfd8e822352c4c8361b757647645b78c8cc74ce885f04c26ee07ff6ada08587a4037363838b1dda6e306091ee0690caa8fe0e6fcd2000000000000006400000040f57f3997a4e81d8f321e9710927e22c2e6d30fb6d8f749a9e4a07afb3b3b7909caefd2ec5f359903d492bc45026b6b45baafe5ad67974e75d8d3e0bb44b704790000000000000064")}
        )

    def test_get_validator_power(self):
        self.assertEqual(
            self.score.get_validator_power(
                bytes.fromhex(
                    "a54ffaa84c8f2f798782de8b962a84784e288487a747813a0857243a60e2ba331db530b76775beb0348c52bb8fc1fdac207525e5689caa01c0af8d2f8f371ec5")
            ),
            100
        )
        self.assertEqual(
            self.score.get_validator_power(
                bytes.fromhex(
                    "724ae29cfeb7497051d09edfd8e822352c4c8361b757647645b78c8cc74ce885f04c26ee07ff6ada08587a4037363838b1dda6e306091ee0690caa8fe0e6fcd2")
            ),
            100
        )
        self.assertEqual(
            self.score.get_validator_power(
                bytes.fromhex(
                    "f57f3997a4e81d8f321e9710927e22c2e6d30fb6d8f749a9e4a07afb3b3b7909caefd2ec5f359903d492bc45026b6b45baafe5ad67974e75d8d3e0bb44b70479")
            ),
            100
        )

    def test_relay_oracle_state_1(self):
        # derive app_hash
        app_hash = multi_store.get_app_hash(
            bytes.fromhex(
                "685430546D23A44E6B8034EAAFBC2F4CD7FEF54B54D5B66528CB4E5225BD74FB") +
            bytes.fromhex(
                "4F8D0BB0CD3EB9DC70B4DBBEA5F0CBD5B523195F7BAE02BB401BB00A93ABA08E") +
            bytes.fromhex(
                "1912057FFF0B3E85ABF1A319F75D37B21B430F3DA7DB9E486A5041DE47C686D3") +
            bytes.fromhex(
                "B1F2FD852E790E735CA2D3014F96A2A53C60393E9C6BBF941B9A6DD6A05CF6F9") +
            bytes.fromhex(
                "91CC906286235B676AD402FC04ED768EB2BFECA664E8D595C286571DA1433C60")
        )

        # derive block_hash
        block_hash = merkle_part.get_block_header(
            bytes.fromhex(
                "32FA694879095840619F5E49380612BD296FF7E950EAFB66FF654D99CA70869E") +
            bytes.fromhex(
                "D9F175396C0E2D0E77F69856ABF5D8E69283CB915EB8886262FEDA1D519B3005") +
            bytes.fromhex(
                "4F4D548668A3986DB253689234B9CAC96303A128B7081B16E53B79AB9E65B887") +
            bytes.fromhex(
                "004209A161040AB1778E2F2C00EE482F205B28EFBA439FCB04EA283F619478D9") +
            bytes.fromhex(
                "6E340B9CFFB37A989CA544E6BB780A2C78901D3FB33738768511A30617AFA01D") +
            bytes.fromhex(
                "D991DA4D4E69473CC75A4B819F9E07D4956671A6F4A74DF4CC16596FCBE68137"),
            app_hash,
            191
        )

        # derive signers
        signers = tm_signature.recover_signers(
            bytes.fromhex("00000003000000209279257914bfee6faec46df086e9a673a4c1576fb299094d45f77e12fa3728e70000002004dbf23f5ebb07ba8fd7ca06843dfe363b5e86596930e1889d9bd5bd3e98fc531c000000106e080211bf0000000000000022480a200000003f12240a2066424e8f0417945a71067a55b7121282a90524e3c0709d8f8addb6adc8fd46d110012a0c08e6e9c6f70510979fbd9801320962616e64636861696e00000020826bb17b714ebcd8199ee2a01334102f19248087cfdeee42ebd406b3991c389500000020621281eedf97f3a9ec121224cef9f8c07872d2c81cce44dd846bb3678dd505231b000000106e080211bf0000000000000022480a200000003f12240a2066424e8f0417945a71067a55b7121282a90524e3c0709d8f8addb6adc8fd46d110012a0c08e6e9c6f70510dd89e98a01320962616e64636861696e00000020d775fd0e1580499ef16a4ab1998dcb4cbd47cf6f342cdc51a9552d1434552ed8000000205a1a2075ae97a6bbd07a5a40efe287eceab37c7a7caae82e6c997c51c62334701b000000106e080211bf0000000000000022480a200000003f12240a2066424e8f0417945a71067a55b7121282a90524e3c0709d8f8addb6adc8fd46d110012a0c08e6e9c6f70510ab94a59201320962616e64636861696e"),
            block_hash
        )

        self.assertEqual(signers, [
            # Ethereum Address 652D89a66Eb4eA55366c45b1f9ACfc8e2179E1c5
            bytes.fromhex(
                "a54ffaa84c8f2f798782de8b962a84784e288487a747813a0857243a60e2ba331db530b76775beb0348c52bb8fc1fdac207525e5689caa01c0af8d2f8f371ec5"),
            # Ethereum Address 88e1cd00710495EEB93D4f522d16bC8B87Cb00FE
            bytes.fromhex(
                "724ae29cfeb7497051d09edfd8e822352c4c8361b757647645b78c8cc74ce885f04c26ee07ff6ada08587a4037363838b1dda6e306091ee0690caa8fe0e6fcd2"),
            # Ethereum Address aAA22E077492CbaD414098EBD98AA8dc1C7AE8D9
            bytes.fromhex(
                "f57f3997a4e81d8f321e9710927e22c2e6d30fb6d8f749a9e4a07afb3b3b7909caefd2ec5f359903d492bc45026b6b45baafe5ad67974e75d8d3e0bb44b70479"),
        ])

    def test_relay_oracle_state_2(self):
        # # derive app_hash
        # app_hash = multi_store.get_app_hash(bytes.fromhex(
        #     "811032f41a5918cfc860ebcea1b7678564c622b4e3f04e28c9d8b195f04661e11e06ea167a89de60abf52c60350793c3823a0a4b9681f59daeb8f20942b8bcf3ff2b888760ffa9efa09e35763d8a5ba3ec794d00bcd1f9a901fa007f1f16e2ebb1f2fd852e790e735ca2d3014f96a2a53c60393e9c6bbf941b9a6dd6a05cf6f9c6507de937080730702a2c39ad8aa4666fd24e12a9496e4546a0bd4031e6d4ee"))

        # print(app_hash)
        # # derive block_hash
        # block_hash = merkle_part.get_block_header(
        #     bytes.fromhex(
        #         "32fa694879095840619f5e49380612bd296ff7e950eafb66ff654d99ca70869e2a448c96300f1cb90567d815c6b2f6ec0bba29615fd88deab57299c76f0b30fa3ebf2264c2c941df347eb97f55b4adcd4784f4f0a8e66d9f2e3fda413115e085004209a161040ab1778e2f2c00ee482f205b28efba439fcb04ea283f619478d96e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d0efe3e12f46363c7779140d4ce659925db52f19053e114d7cc4efd666b37f79f"),
        #     app_hash,
        #     1412
        # )

        # # derive signers
        # signers = tm_signature.recover_signers(
        #     bytes.fromhex("0000000300000020628716ac49023de84adddddcbef8007c2e41e5b58306ce87a0afad5447bc6210000000202f520db2bff3003d5612e03b7aaa99472164c73922a977af95e1ffc2a67c53b41b000000106e080211840500000000000022480a200000003f12240a2066424e8f0417945a71067a55b7121282a90524e3c0709d8f8addb6adc8fd46d110012a0c08e6e9c6f70510979fbd9801320962616e64636861696e00000020ff2ba7e2bd2175827997c706451b5da768b6873d7ba4129fc6ee54e62ba9c593000000203c7f7e5b08d1733d430658431545c9a2f57e4641b3b4cd52e567f27be9485e601c000000106e080211840500000000000022480a200000003f12240a20b8aac9c5f107c71eacda8ccddd2506f30ecfa75685e12e403ddcc6411f6822ff10012a0c088d92c7f70510a3f0e5be02320962616e64636861696e000000205a2f66b4d62d905b98277cd2807a324f0651340e80ae0249e500beb5ddcdce11000000203c1ed3d960b19e0ca7d321215874c6e91407ae3d2748f2e3b617fad833c30b6d1b000000106e080211840500000000000022480a200000003f12240a20b8aac9c5f107c71eacda8ccddd2506f30ecfa75685e12e403ddcc6411f6822ff10012a0c088d92c7f70510a394a6bf02320962616e64636861696e"),
        #     block_hash
        # )

        # print("≤≥≤≥≤≥≤≥≤≥≤≥≤≥≤≥≤≥≤≥≤≥≤≥≤≥≤≥")
        # print([x.hex() for x in signers])

        pass

        # self.assertEqual(signers, [
        #     # Ethereum Address 652D89a66Eb4eA55366c45b1f9ACfc8e2179E1c5
        #     bytes.fromhex(
        #         "a54ffaa84c8f2f798782de8b962a84784e288487a747813a0857243a60e2ba331db530b76775beb0348c52bb8fc1fdac207525e5689caa01c0af8d2f8f371ec5"),
        #     # Ethereum Address 88e1cd00710495EEB93D4f522d16bC8B87Cb00FE
        #     bytes.fromhex(
        #         "724ae29cfeb7497051d09edfd8e822352c4c8361b757647645b78c8cc74ce885f04c26ee07ff6ada08587a4037363838b1dda6e306091ee0690caa8fe0e6fcd2"),
        #     # Ethereum Address aAA22E077492CbaD414098EBD98AA8dc1C7AE8D9
        #     bytes.fromhex(
        #         "f57f3997a4e81d8f321e9710927e22c2e6d30fb6d8f749a9e4a07afb3b3b7909caefd2ec5f359903d492bc45026b6b45baafe5ad67974e75d8d3e0bb44b70479"),
        # ])

    # fail because there is no correspond oracle state
    # NO_ORACLE_ROOT_STATE_DATA
    def test_verify_oracle_data_fail_1(self):
        self.assertRaises(
            IconScoreException,
            lambda x: self.score.verify_oracle_data(*x),
            (
                182,
                bytes.fromhex("000000046265656200000000000000010000000f0000000342544300000000000003e800000000000000040000000000000004000000046265656200000000000000010000000000000004000000005edddcd3000000005edddcd700000001000000080000000000948e69"),
                163,
                bytes.fromhex(
                    "000000060102000000000000000300000000000000b4000000204d4479f8cf02cba65f95231b06eeaa51e99f75a153c3ed28d9a86b565de593060103000000000000000500000000000000b4000000208861ad25f99a677d4934541a99928cdbe18bbf34ee39d754e93cce090be705020104000000000000000900000000000000b4000000205d162c955ae030390cea63ca7ed8ba72b7a49e0bc73daea23cf6b79e8899c49c0105000000000000001000000000000000b40000002008dd24b96c3c9413ba46a7149232c18ad66db68ac04cf2a770b707b6d29fc8f70106000000000000001800000000000000b40000002032d2e1cc89f3fbd139c35b5d5fe6430799aeefd495c882c419a120b7257e3f5a0107000000000000003e00000000000000b500000020691b2504cd253868bccd43774c8b8dbfa1e2d0d41c07c23f2f1237fcf0d2f0d8")
            )
        )

    # fail because of wrong proof
    # INVALID_ORACLE_DATA_PROOF

    def test_verify_oracle_data_fail_2(self):
        self.score.set_oracle_state(
            182,
            bytes.fromhex(
                "B59AD73DB9147F6AC7C88A64B1BAD51C90F8C48B4487ADA9276A323808E56E3E")
        )

        with self.assertRaises(IconScoreException) as e:
            self.score.verify_oracle_data(
                182,
                # client_id should be beeb(62656562) not beee(62656565)
                bytes.fromhex("000000046265656500000000000000010000000f0000000342544300000000000003e800000000000000040000000000000004000000046265656200000000000000010000000000000004000000005edddcd3000000005edddcd700000001000000080000000000948e69"),
                163,
                bytes.fromhex(
                    "000000060102000000000000000300000000000000b4000000204d4479f8cf02cba65f95231b06eeaa51e99f75a153c3ed28d9a86b565de593060103000000000000000500000000000000b4000000208861ad25f99a677d4934541a99928cdbe18bbf34ee39d754e93cce090be705020104000000000000000900000000000000b4000000205d162c955ae030390cea63ca7ed8ba72b7a49e0bc73daea23cf6b79e8899c49c0105000000000000001000000000000000b40000002008dd24b96c3c9413ba46a7149232c18ad66db68ac04cf2a770b707b6d29fc8f70106000000000000001800000000000000b40000002032d2e1cc89f3fbd139c35b5d5fe6430799aeefd495c882c419a120b7257e3f5a0107000000000000003e00000000000000b500000020691b2504cd253868bccd43774c8b8dbfa1e2d0d41c07c23f2f1237fcf0d2f0d8")
            )

        self.assertEqual(e.exception.code, 32)
        self.assertEqual(e.exception.message, "INVALID_ORACLE_DATA_PROOF")

    def test_verify_oracle_data_success(self):
        self.score.set_oracle_state(
            182,
            bytes.fromhex(
                "B59AD73DB9147F6AC7C88A64B1BAD51C90F8C48B4487ADA9276A323808E56E3E")
        )
        packet = self.score.verify_oracle_data(
            182,
            bytes.fromhex("000000046265656200000000000000010000000f0000000342544300000000000003e800000000000000040000000000000004000000046265656200000000000000010000000000000004000000005edddcd3000000005edddcd700000001000000080000000000948e69"),
            163,
            bytes.fromhex(
                "000000060102000000000000000300000000000000b4000000204d4479f8cf02cba65f95231b06eeaa51e99f75a153c3ed28d9a86b565de593060103000000000000000500000000000000b4000000208861ad25f99a677d4934541a99928cdbe18bbf34ee39d754e93cce090be705020104000000000000000900000000000000b4000000205d162c955ae030390cea63ca7ed8ba72b7a49e0bc73daea23cf6b79e8899c49c0105000000000000001000000000000000b40000002008dd24b96c3c9413ba46a7149232c18ad66db68ac04cf2a770b707b6d29fc8f70106000000000000001800000000000000b40000002032d2e1cc89f3fbd139c35b5d5fe6430799aeefd495c882c419a120b7257e3f5a0107000000000000003e00000000000000b500000020691b2504cd253868bccd43774c8b8dbfa1e2d0d41c07c23f2f1237fcf0d2f0d8")
        )
        self.assertEqual(packet["req"]["ask_count"], 4)
        self.assertEqual(
            packet["req"]["calldata"], b'\x00\x00\x00\x03BTC\x00\x00\x00\x00\x00\x00\x03\xe8')
        self.assertEqual(packet["req"]["client_id"], 'beeb')
        self.assertEqual(packet["req"]["min_count"], 4)
        self.assertEqual(packet["req"]["oracle_script_id"], 1)

        self.assertEqual(packet["res"]["client_id"], 'beeb')
        self.assertEqual(packet["res"]["ans_count"], 4)
        self.assertEqual(packet["res"]["request_id"], 1)
        self.assertEqual(packet["res"]["request_time"], 1591598291)
        self.assertEqual(packet["res"]["resolve_time"], 1591598295)
        self.assertEqual(packet["res"]["resolve_status"], 0)
        self.assertEqual(packet["res"]["result"],
                         b'\x00\x00\x08\x00\x00\x00\x00\x00\x94\x8ei')

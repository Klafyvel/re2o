# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-30 15:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import preferences.models
import re2o.aes_field


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0001_model_creation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_model_creation'),
        ('preferences', '0001_model_creation'),
        ('reversion', '0001_squashed_0004_auto_20160611_1202'),
    ]
    replaces = [
        ("users", "0001_initial"),
        ("users", "0002_auto_20160630_2301"),
        ("users", "0003_listrights_rights"),
        ("users", "0004_auto_20160701_2312"),
        ("users", "0005_auto_20160702_0006"),
        ("users", "0006_ban"),
        ("users", "0007_auto_20160702_2322"),
        ("users", "0008_user_registered"),
        ("users", "0009_user_room"),
        ("users", "0010_auto_20160703_1226"),
        ("users", "0011_auto_20160703_1227"),
        ("users", "0012_auto_20160703_1230"),
        ("users", "0013_auto_20160704_1547"),
        ("users", "0014_auto_20160704_1548"),
        ("users", "0015_whitelist"),
        ("users", "0016_auto_20160706_1220"),
        ("users", "0017_auto_20160707_0105"),
        ("users", "0018_auto_20160707_0115"),
        ("users", "0019_auto_20160708_1633"),
        ("users", "0020_request"),
        ("users", "0021_ldapuser"),
        ("users", "0022_ldapuser_sambasid"),
        ("users", "0023_auto_20160724_1908"),
        ("users", "0024_remove_ldapuser_mac_list"),
        ("users", "0025_listshell"),
        ("users", "0026_user_shell"),
        ("users", "0027_auto_20160726_0216"),
        ("users", "0028_auto_20160726_0227"),
        ("users", "0029_auto_20160726_0229"),
        ("users", "0030_auto_20160726_0357"),
        ("users", "0031_auto_20160726_0359"),
        ("users", "0032_auto_20160727_2122"),
        ("users", "0033_remove_ldapuser_loginshell"),
        ("users", "0034_auto_20161018_0037"),
        ("users", "0035_auto_20161018_0046"),
        ("users", "0036_auto_20161022_2146"),
        ("users", "0037_auto_20161028_1906"),
        ("users", "0038_auto_20161031_0258"),
        ("users", "0039_auto_20161119_0033"),
        ("users", "0040_auto_20161119_1709"),
        ("users", "0041_listright_details"),
        ("users", "0042_auto_20161126_2028"),
        ("users", "0043_auto_20161224_1156"),
        ("users", "0043_ban_state"),
        ("users", "0044_user_ssh_public_key"),
        ("users", "0045_merge"),
        ("users", "0046_auto_20170617_1433"),
        ("users", "0047_auto_20170618_0156"),
        ("users", "0048_auto_20170618_0210"),
        ("users", "0049_auto_20170618_1424"),
        ("users", "0050_serviceuser_comment"),
        ("users", "0051_user_telephone"),
        ("users", "0052_ldapuser_shadowexpire"),
        ("users", "0053_auto_20170626_2105"),
        ("users", "0054_auto_20170626_2219"),
        ("users", "0055_auto_20171003_0556"),
        ("users", "0056_auto_20171015_2033"),
        ("users", "0057_auto_20171023_0301"),
        ("users", "0058_auto_20171025_0154"),
        ("users", "0059_auto_20171025_1854"),
        ("users", "0060_auto_20171120_0317"),
        ("users", "0061_auto_20171230_2033"),
        ("users", "0062_auto_20171231_0056"),
        ("users", "0063_auto_20171231_0140"),
        ("users", "0064_auto_20171231_0150"),
        ("users", "0065_auto_20171231_2053"),
        ("users", "0066_grouppermissions"),
        ("users", "0067_serveurpermission"),
        ("users", "0068_auto_20180107_2245"),
        ("users", "0069_club_mailing"),
        ("users", "0070_auto_20180324_1906"),
        ("users", "0071_auto_20180415_1252"),
        ("users", "0072_auto_20180426_2021"),
        ("users", "0073_auto_20180629_1614"),
        ("users", "0074_auto_20180810_2104"),
        ("users", "0074_auto_20180814_1059"),
        ("users", "0075_merge_20180815_2202"),
        ("users", "0076_auto_20180818_1321"),
        ("users", "0077_auto_20180824_1750"),
        ("users", "0078_auto_20181011_1405"),
        ("users", "0079_auto_20181228_2039"),
        ("users", "0080_auto_20190108_1726"),
        ("users", "0081_auto_20190317_0302"),
        ("users", "0082_auto_20190908_1338"),
        ("users", "0083_user_shortcuts_enabled"),
        ("users", "0084_auto_20191120_0159"),
        ("users", "0085_user_email_state"),
        ("users", "0086_user_email_change_date"),
        ("users", "0087_request_email"),
        ("users", "0088_auto_20200417_2312"),
        ("users", "0089_auto_20200418_0112"),
        ("users", "0090_auto_20200421_1825"),
        ("users", "0091_auto_20200423_1256"),
        ("users", "0092_auto_20200502_0057"),
        ("users", "0093_user_profile_image"),
        ("users", "0094_remove_user_profile_image"),
        ("users", "0095_user_theme"),
        ("cotisations", "0001_initial"),
        ("cotisations", "0002_remove_facture_article"),
        ("cotisations", "0003_auto_20160702_1448"),
        ("cotisations", "0004_auto_20160702_1528"),
        ("cotisations", "0005_auto_20160702_1532"),
        ("cotisations", "0006_auto_20160702_1534"),
        ("cotisations", "0007_auto_20160702_1543"),
        ("cotisations", "0008_auto_20160702_1614"),
        ("cotisations", "0009_remove_cotisation_user"),
        ("cotisations", "0010_auto_20160702_1840"),
        ("cotisations", "0011_auto_20160702_1911"),
        ("cotisations", "0012_auto_20160704_0118"),
        ("cotisations", "0013_auto_20160711_2240"),
        ("cotisations", "0014_auto_20160712_0245"),
        ("cotisations", "0015_auto_20160714_2142"),
        ("cotisations", "0016_auto_20160715_0110"),
        ("cotisations", "0017_auto_20170718_2329"),
        ("cotisations", "0018_paiement_type_paiement"),
        ("cotisations", "0019_auto_20170819_0055"),
        ("cotisations", "0020_auto_20170819_0057"),
        ("cotisations", "0021_auto_20170819_0104"),
        ("cotisations", "0022_auto_20170824_0128"),
        ("cotisations", "0023_auto_20170902_1303"),
        ("cotisations", "0024_auto_20171015_2033"),
        ("cotisations", "0025_article_type_user"),
        ("cotisations", "0026_auto_20171028_0126"),
        ("cotisations", "0027_auto_20171029_1156"),
        ("cotisations", "0028_auto_20171231_0007"),
        ("cotisations", "0029_auto_20180414_2056"),
        ("cotisations", "0030_custom_payment"),
        ("cotisations", "0031_comnpaypayment_production"),
        ("cotisations", "0032_custom_invoice"),
        ("cotisations", "0033_auto_20180818_1319"),
        ("cotisations", "0034_auto_20180831_1532"),
        ("cotisations", "0035_notepayment"),
        ("cotisations", "0036_custominvoice_remark"),
        ("cotisations", "0037_costestimate"),
        ("cotisations", "0038_auto_20181231_1657"),
        ("cotisations", "0039_freepayment"),
        ("cotisations", "0040_auto_20191002_2335"),
        ("cotisations", "0041_auto_20191103_2131"),
        ("cotisations", "0042_auto_20191120_0159"),
        ("cotisations", "0043_separation_membership_connection_p1"),
        ("cotisations", "0044_separation_membership_connection_p2"),
        ("cotisations", "0045_separation_membership_connection_p3"),
        ("cotisations", "0046_article_need_membership"),
        ("cotisations", "0047_article_need_membership_init"),
        ("cotisations", "0048_auto_20201017_0018"),
        ("cotisations", "0049_auto_20201102_2305"),
        ("cotisations", "0050_auto_20201102_2342"),
        ("cotisations", "0051_auto_20201228_1636"),
        ("machines", "0001_initial"),
        ("machines", "0002_auto_20160703_1444"),
        ("machines", "0003_auto_20160703_1450"),
        ("machines", "0004_auto_20160703_1451"),
        ("machines", "0005_auto_20160703_1523"),
        ("machines", "0006_auto_20160703_1813"),
        ("machines", "0007_auto_20160703_1816"),
        ("machines", "0008_remove_interface_ipv6"),
        ("machines", "0009_auto_20160703_2358"),
        ("machines", "0010_auto_20160704_0104"),
        ("machines", "0011_auto_20160704_0105"),
        ("machines", "0012_auto_20160704_0118"),
        ("machines", "0013_auto_20160705_1014"),
        ("machines", "0014_auto_20160706_1220"),
        ("machines", "0015_auto_20160707_0105"),
        ("machines", "0016_auto_20160708_1633"),
        ("machines", "0017_auto_20160708_1645"),
        ("machines", "0018_auto_20160708_1813"),
        ("machines", "0019_auto_20160718_1141"),
        ("machines", "0020_auto_20160718_1849"),
        ("machines", "0021_auto_20161006_1943"),
        ("machines", "0022_auto_20161011_1829"),
        ("machines", "0023_iplist_ip_type"),
        ("machines", "0024_machinetype_need_infra"),
        ("machines", "0025_auto_20161023_0038"),
        ("machines", "0026_auto_20161026_1348"),
        ("machines", "0027_alias"),
        ("machines", "0028_iptype_domaine_ip"),
        ("machines", "0029_iptype_domaine_range"),
        ("machines", "0030_auto_20161118_1730"),
        ("machines", "0031_auto_20161119_1709"),
        ("machines", "0032_auto_20161119_1850"),
        ("machines", "0033_extension_need_infra"),
        ("machines", "0034_iplist_need_infra"),
        ("machines", "0035_auto_20161224_1201"),
        ("machines", "0036_auto_20161224_1204"),
        ("machines", "0037_domain_cname"),
        ("machines", "0038_auto_20161224_1721"),
        ("machines", "0039_auto_20161224_1732"),
        ("machines", "0040_remove_interface_dns"),
        ("machines", "0041_remove_ns_interface"),
        ("machines", "0042_ns_ns"),
        ("machines", "0043_auto_20170721_0350"),
        ("machines", "0044_auto_20170808_0233"),
        ("machines", "0045_auto_20170808_0348"),
        ("machines", "0046_auto_20170808_1423"),
        ("machines", "0047_auto_20170809_0606"),
        ("machines", "0048_auto_20170823_2315"),
        ("machines", "0049_vlan"),
        ("machines", "0050_auto_20170826_0022"),
        ("machines", "0051_iptype_vlan"),
        ("machines", "0052_auto_20170828_2322"),
        ("machines", "0053_text"),
        ("machines", "0054_text_zone"),
        ("machines", "0055_nas"),
        ("machines", "0056_nas_port_access_mode"),
        ("machines", "0057_nas_autocapture_mac"),
        ("machines", "0058_auto_20171002_0350"),
        ("machines", "0059_iptype_prefix_v6"),
        ("machines", "0060_iptype_ouverture_ports"),
        ("machines", "0061_auto_20171015_2033"),
        ("machines", "0062_extension_origin_v6"),
        ("machines", "0063_auto_20171020_0040"),
        ("machines", "0064_auto_20171115_0253"),
        ("machines", "0065_auto_20171115_1514"),
        ("machines", "0066_srv"),
        ("machines", "0067_auto_20171116_0152"),
        ("machines", "0068_auto_20171116_0252"),
        ("machines", "0069_auto_20171116_0822"),
        ("machines", "0070_auto_20171231_1947"),
        ("machines", "0071_auto_20171231_2100"),
        ("machines", "0072_auto_20180108_1822"),
        ("machines", "0073_auto_20180128_2203"),
        ("machines", "0074_auto_20180129_0352"),
        ("machines", "0075_auto_20180130_0052"),
        ("machines", "0076_auto_20180130_1623"),
        ("machines", "0077_auto_20180409_2243"),
        ("machines", "0078_auto_20180415_1252"),
        ("machines", "0079_auto_20180416_0107"),
        ("machines", "0080_auto_20180502_2334"),
        ("machines", "0081_auto_20180521_1413"),
        ("machines", "0082_auto_20180525_2209"),
        ("machines", "0083_remove_duplicate_rights"),
        ("machines", "0084_dname"),
        ("machines", "0085_sshfingerprint"),
        ("machines", "0086_role"),
        ("machines", "0087_dnssec"),
        ("machines", "0088_iptype_prefix_v6_length"),
        ("machines", "0089_auto_20180805_1148"),
        ("machines", "0090_auto_20180805_1459"),
        ("machines", "0091_auto_20180806_2310"),
        ("machines", "0092_auto_20180807_0926"),
        ("machines", "0093_auto_20180807_1115"),
        ("machines", "0094_auto_20180815_1918"),
        ("machines", "0095_auto_20180919_2225"),
        ("machines", "0096_auto_20181013_1417"),
        ("machines", "0097_extension_dnssec"),
        ("machines", "0098_auto_20190102_1745"),
        ("machines", "0099_role_recursive_dns"),
        ("machines", "0100_auto_20190102_1753"),
        ("machines", "0101_auto_20190108_1623"),
        ("machines", "0102_auto_20190303_1611"),
        ("machines", "0103_auto_20191002_2222"),
        ("machines", "0104_auto_20191002_2231"),
        ("machines", "0105_dname_ttl"),
        ("machines", "0106_auto_20191120_0159"),
        ("machines", "0107_fix_lowercase_domain"),
        ("machines", "0108_ipv6list_active"),
        ("preferences", "0001_initial"),
        ("preferences", "0002_auto_20170625_1923"),
        ("preferences", "0003_optionaluser_solde_negatif"),
        ("preferences", "0004_assooption_services"),
        ("preferences", "0005_auto_20170824_0139"),
        ("preferences", "0006_auto_20170824_0143"),
        ("preferences", "0007_auto_20170824_2056"),
        ("preferences", "0008_auto_20170824_2122"),
        ("preferences", "0009_assooption_utilisateur_asso"),
        ("preferences", "0010_auto_20170825_0459"),
        ("preferences", "0011_auto_20170825_2307"),
        ("preferences", "0012_generaloption_req_expire_hrs"),
        ("preferences", "0013_generaloption_site_name"),
        ("preferences", "0014_generaloption_email_from"),
        ("preferences", "0015_optionaltopologie_radius_general_policy"),
        ("preferences", "0016_auto_20170902_1520"),
        ("preferences", "0017_mailmessageoption"),
        ("preferences", "0018_optionaltopologie_mac_autocapture"),
        ("preferences", "0019_remove_optionaltopologie_mac_autocapture"),
        ("preferences", "0020_optionalmachine_ipv6"),
        ("preferences", "0021_auto_20171015_1741"),
        ("preferences", "0022_auto_20171015_1758"),
        ("preferences", "0023_auto_20171015_2033"),
        ("preferences", "0024_optionaluser_all_can_create"),
        ("preferences", "0025_auto_20171231_2142"),
        ("preferences", "0025_generaloption_general_message"),
        ("preferences", "0026_auto_20171216_0401"),
        ("preferences", "0027_merge_20180106_2019"),
        ("preferences", "0028_assooption_description"),
        ("preferences", "0028_auto_20180111_1129"),
        ("preferences", "0028_auto_20180128_2203"),
        ("preferences", "0029_auto_20180111_1134"),
        ("preferences", "0029_auto_20180318_0213"),
        ("preferences", "0029_auto_20180318_1005"),
        ("preferences", "0030_auto_20180111_2346"),
        ("preferences", "0030_merge_20180320_1419"),
        ("preferences", "0031_auto_20180323_0218"),
        ("preferences", "0031_optionaluser_self_adhesion"),
        ("preferences", "0032_optionaluser_min_online_payment"),
        ("preferences", "0032_optionaluser_shell_default"),
        ("preferences", "0033_accueiloption"),
        ("preferences", "0033_generaloption_gtu_sum_up"),
        ("preferences", "0034_auto_20180114_2025"),
        ("preferences", "0034_auto_20180416_1120"),
        ("preferences", "0035_auto_20180114_2132"),
        ("preferences", "0035_optionaluser_allow_self_subscription"),
        ("preferences", "0036_auto_20180114_2141"),
        ("preferences", "0037_auto_20180114_2156"),
        ("preferences", "0038_auto_20180114_2209"),
        ("preferences", "0039_auto_20180115_0003"),
        ("preferences", "0040_auto_20180129_1745"),
        ("preferences", "0041_merge_20180130_0052"),
        ("preferences", "0042_auto_20180222_1743"),
        ("preferences", "0043_optionalmachine_create_machine"),
        ("preferences", "0044_remove_payment_pass"),
        ("preferences", "0045_remove_unused_payment_fields"),
        ("preferences", "0046_optionaluser_mail_extension"),
        ("preferences", "0047_mailcontact"),
        ("preferences", "0048_auto_20180811_1515"),
        ("preferences", "0049_optionaluser_self_change_shell"),
        ("preferences", "0050_auto_20180818_1329"),
        ("preferences", "0051_auto_20180919_2225"),
        ("preferences", "0052_optionaluser_delete_notyetactive"),
        ("preferences", "0053_optionaluser_self_change_room"),
        ("preferences", "0055_generaloption_main_site_url"),
        ("preferences", "0056_1_radiusoption"),
        ("preferences", "0056_2_radiusoption"),
        ("preferences", "0056_3_radiusoption"),
        ("preferences", "0056_4_radiusoption"),
        ("preferences", "0057_optionaluser_all_users_active"),
        ("preferences", "0058_auto_20190108_1650"),
        ("preferences", "0059_auto_20190120_1739"),
        ("preferences", "0060_auto_20190712_1821"),
        ("preferences", "0061_optionaluser_allow_archived_connexion"),
        ("preferences", "0062_auto_20190910_1909"),
        ("preferences", "0063_mandate"),
        ("preferences", "0064_auto_20191008_1335"),
        ("preferences", "0065_auto_20191010_1227"),
        ("preferences", "0066_optionalmachine_default_dns_ttl"),
        ("preferences", "0067_auto_20191120_0159"),
        ("preferences", "0068_optionaluser_allow_set_password_during_user_creation"),
        ("preferences", "0069_optionaluser_disable_emailnotyetconfirmed"),
        ("preferences", "0070_auto_20200419_0225"),
        ("preferences", "0071_optionaluser_self_change_pseudo"),
        ("topologie", "0001_initial"),
        ("topologie", "0002_auto_20160703_1118"),
        ("topologie", "0003_room"),
        ("topologie", "0004_auto_20160703_1122"),
        ("topologie", "0005_auto_20160703_1123"),
        ("topologie", "0006_auto_20160703_1129"),
        ("topologie", "0007_auto_20160703_1148"),
        ("topologie", "0008_port_room"),
        ("topologie", "0009_auto_20160703_1200"),
        ("topologie", "0010_auto_20160704_2148"),
        ("topologie", "0011_auto_20160704_2153"),
        ("topologie", "0012_port_machine_interface"),
        ("topologie", "0013_port_related"),
        ("topologie", "0014_auto_20160706_1238"),
        ("topologie", "0015_auto_20160706_1452"),
        ("topologie", "0016_auto_20160706_1531"),
        ("topologie", "0017_auto_20160718_1141"),
        ("topologie", "0018_room_details"),
        ("topologie", "0019_auto_20161026_1348"),
        ("topologie", "0020_auto_20161119_0033"),
        ("topologie", "0021_port_radius"),
        ("topologie", "0022_auto_20161211_1622"),
        ("topologie", "0023_auto_20170817_1654"),
        ("topologie", "0023_auto_20170826_1530"),
        ("topologie", "0024_auto_20170818_1021"),
        ("topologie", "0024_auto_20170826_1800"),
        ("topologie", "0025_merge_20170902_1242"),
        ("topologie", "0026_auto_20170902_1245"),
        ("topologie", "0027_auto_20170905_1442"),
        ("topologie", "0028_auto_20170913_1503"),
        ("topologie", "0029_auto_20171002_0334"),
        ("topologie", "0030_auto_20171004_0235"),
        ("topologie", "0031_auto_20171015_2033"),
        ("topologie", "0032_auto_20171026_0338"),
        ("topologie", "0033_auto_20171231_1743"),
        ("topologie", "0034_borne"),
        ("topologie", "0035_auto_20180324_0023"),
        ("topologie", "0036_transferborne"),
        ("topologie", "0037_auto_20180325_0127"),
        ("topologie", "0038_transfersw"),
        ("topologie", "0039_port_new_switch"),
        ("topologie", "0040_transferports"),
        ("topologie", "0041_transferportsw"),
        ("topologie", "0042_transferswitch"),
        ("topologie", "0043_renamenewswitch"),
        ("topologie", "0044_auto_20180326_0002"),
        ("topologie", "0045_auto_20180326_0123"),
        ("topologie", "0046_auto_20180326_0129"),
        ("topologie", "0047_ap_machine"),
        ("topologie", "0048_ap_machine"),
        ("topologie", "0049_switchs_machine"),
        ("topologie", "0050_port_new_switch"),
        ("topologie", "0051_switchs_machine"),
        ("topologie", "0052_transferports"),
        ("topologie", "0053_finalsw"),
        ("topologie", "0054_auto_20180326_1742"),
        ("topologie", "0055_auto_20180329_0431"),
        ("topologie", "0056_building_switchbay"),
        ("topologie", "0057_auto_20180408_0316"),
        ("topologie", "0058_remove_switch_location"),
        ("topologie", "0059_auto_20180415_2249"),
        ("topologie", "0060_server"),
        ("topologie", "0061_portprofile"),
        ("topologie", "0062_auto_20180815_1918"),
        ("topologie", "0063_auto_20180919_2225"),
        ("topologie", "0064_switch_automatic_provision"),
        ("topologie", "0065_auto_20180927_1836"),
        ("topologie", "0066_modelswitch_commercial_name"),
        ("topologie", "0067_auto_20181230_1819"),
        ("topologie", "0068_auto_20190102_1758"),
        ("topologie", "0069_auto_20190108_1439"),
        ("topologie", "0070_auto_20190218_1743"),
        ("topologie", "0071_auto_20190218_1936"),
        ("topologie", "0072_auto_20190720_2318"),
        ("topologie", "0073_auto_20191120_0159"),
        ("topologie", "0074_auto_20200419_1640"),
            ]

    operations = [
        migrations.AddField(
            model_name='assooption',
            name='utilisateur_asso',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cotisationsoption',
            name='invoice_template',
            field=models.OneToOneField(default=preferences.models.default_invoice, on_delete=django.db.models.deletion.PROTECT, related_name='invoice_template', to='preferences.DocumentTemplate', verbose_name='template for invoices'),
        ),
        migrations.AddField(
            model_name='cotisationsoption',
            name='voucher_template',
            field=models.OneToOneField(default=preferences.models.default_voucher, on_delete=django.db.models.deletion.PROTECT, related_name='voucher_template', to='preferences.DocumentTemplate', verbose_name='template for subscription vouchers'),
        ),
        migrations.AddField(
            model_name='mandate',
            name='president',
            field=models.ForeignKey(blank=True, help_text='Displayed on subscription vouchers.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='president of the association'),
        ),
        migrations.AddField(
            model_name='optionaltopologie',
            name='switchs_ip_type',
            field=models.OneToOneField(blank=True, help_text='IP range for the management of switches.', null=True, on_delete=django.db.models.deletion.PROTECT, to='machines.IpType'),
        ),
        migrations.AddField(
            model_name='optionaluser',
            name='shell_default',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.ListShell'),
        ),
        migrations.AddField(
            model_name='radiusoption',
            name='banned_attributes',
            field=models.ManyToManyField(blank=True, help_text='Answer attributes for banned users.', related_name='banned_attribute', to='preferences.RadiusAttribute', verbose_name='banned users attributes'),
        ),
        migrations.AddField(
            model_name='radiusoption',
            name='banned_vlan',
            field=models.ForeignKey(blank=True, help_text='VLAN for banned users if not rejected.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='banned_vlan', to='machines.Vlan', verbose_name='banned users VLAN'),
        ),
        migrations.AddField(
            model_name='radiusoption',
            name='non_member_attributes',
            field=models.ManyToManyField(blank=True, help_text='Answer attributes for non members.', related_name='non_member_attribute', to='preferences.RadiusAttribute', verbose_name='non members attributes'),
        ),
        migrations.AddField(
            model_name='radiusoption',
            name='non_member_vlan',
            field=models.ForeignKey(blank=True, help_text='VLAN for non members if not rejected.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='non_member_vlan', to='machines.Vlan', verbose_name='non members VLAN'),
        ),
        migrations.AddField(
            model_name='radiusoption',
            name='ok_attributes',
            field=models.ManyToManyField(blank=True, help_text='Answer attributes for accepted users.', related_name='ok_attribute', to='preferences.RadiusAttribute', verbose_name='accepted users attributes'),
        ),
        migrations.AddField(
            model_name='radiusoption',
            name='unknown_machine_attributes',
            field=models.ManyToManyField(blank=True, help_text='Answer attributes for unknown machines.', related_name='unknown_machine_attribute', to='preferences.RadiusAttribute', verbose_name='unknown machines attributes'),
        ),
        migrations.AddField(
            model_name='radiusoption',
            name='unknown_machine_vlan',
            field=models.ForeignKey(blank=True, help_text='VLAN for unknown machines if not rejected.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unknown_machine_vlan', to='machines.Vlan', verbose_name='unknown machines VLAN'),
        ),
        migrations.AddField(
            model_name='radiusoption',
            name='unknown_port_attributes',
            field=models.ManyToManyField(blank=True, help_text='Answer attributes for unknown ports.', related_name='unknown_port_attribute', to='preferences.RadiusAttribute', verbose_name='unknown ports attributes'),
        ),
        migrations.AddField(
            model_name='radiusoption',
            name='unknown_port_vlan',
            field=models.ForeignKey(blank=True, help_text='VLAN for unknown ports if not rejected.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unknown_port_vlan', to='machines.Vlan', verbose_name='unknown ports VLAN'),
        ),
        migrations.AddField(
            model_name='radiusoption',
            name='unknown_room_attributes',
            field=models.ManyToManyField(blank=True, help_text='Answer attributes for unknown rooms.', related_name='unknown_room_attribute', to='preferences.RadiusAttribute', verbose_name='unknown rooms attributes'),
        ),
        migrations.AddField(
            model_name='radiusoption',
            name='unknown_room_vlan',
            field=models.ForeignKey(blank=True, help_text='VLAN for unknown rooms if not rejected.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unknown_room_vlan', to='machines.Vlan', verbose_name='unknown rooms VLAN'),
        ),
        migrations.AddField(
            model_name='radiusoption',
            name='vlan_decision_ok',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vlan_ok_option', to='machines.Vlan'),
        ),
    ]

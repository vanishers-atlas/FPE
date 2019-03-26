#include "header.h"


// **** Fire function declaration **** //
static inline void butterfly_sharecoe(int i0, int i1, int *o0, int *o1, int W) {
asm ("ADDMULSRA1 %[A0], %[b0], %[w0], %[a0]\n\t"
     "SUBMULSRA1 %[B0], %[b0], %[w0], %[a0]\n\t"
     : [A0]"=&r"(*o0), [B0]"=&r"(*o1)
     : [b0]"r"(i1), [w0]"i"(W), [a0]"r"(i0)
      );
}

// **** Main function **** //
void FPE5PE0() {

  // **** Variable declaration **** //
	int T1280_i0;
	int T1280_i1;
	int T1280_o0;
	int T1280_o1;
	int T1280_W;

	int T1281_i0;
	int T1281_i1;
	int T1281_o0;
	int T1281_o1;
	int T1281_W;

	int T1282_i0;
	int T1282_i1;
	int T1282_o0;
	int T1282_o1;
	int T1282_W;

	int T1283_i0;
	int T1283_i1;
	int T1283_o0;
	int T1283_o1;
	int T1283_W;

	int T1284_i0;
	int T1284_i1;
	int T1284_o0;
	int T1284_o1;
	int T1284_W;

	int T1285_i0;
	int T1285_i1;
	int T1285_o0;
	int T1285_o1;
	int T1285_W;

	int T1286_i0;
	int T1286_i1;
	int T1286_o0;
	int T1286_o1;
	int T1286_W;

	int T1287_i0;
	int T1287_i1;
	int T1287_o0;
	int T1287_o1;
	int T1287_W;

	int T1288_i0;
	int T1288_i1;
	int T1288_o0;
	int T1288_o1;
	int T1288_W;

	int T1289_i0;
	int T1289_i1;
	int T1289_o0;
	int T1289_o1;
	int T1289_W;

	int T1290_i0;
	int T1290_i1;
	int T1290_o0;
	int T1290_o1;
	int T1290_W;

	int T1291_i0;
	int T1291_i1;
	int T1291_o0;
	int T1291_o1;
	int T1291_W;

	int T1292_i0;
	int T1292_i1;
	int T1292_o0;
	int T1292_o1;
	int T1292_W;

	int T1293_i0;
	int T1293_i1;
	int T1293_o0;
	int T1293_o1;
	int T1293_W;

	int T1294_i0;
	int T1294_i1;
	int T1294_o0;
	int T1294_o1;
	int T1294_W;

	int T1295_i0;
	int T1295_i1;
	int T1295_o0;
	int T1295_o1;
	int T1295_W;

	int T1296_i0;
	int T1296_i1;
	int T1296_o0;
	int T1296_o1;
	int T1296_W;

	int T1297_i0;
	int T1297_i1;
	int T1297_o0;
	int T1297_o1;
	int T1297_W;

	int T1298_i0;
	int T1298_i1;
	int T1298_o0;
	int T1298_o1;
	int T1298_W;

	int T1299_i0;
	int T1299_i1;
	int T1299_o0;
	int T1299_o1;
	int T1299_W;

	int T1300_i0;
	int T1300_i1;
	int T1300_o0;
	int T1300_o1;
	int T1300_W;

	int T1301_i0;
	int T1301_i1;
	int T1301_o0;
	int T1301_o1;
	int T1301_W;

	int T1302_i0;
	int T1302_i1;
	int T1302_o0;
	int T1302_o1;
	int T1302_W;

	int T1303_i0;
	int T1303_i1;
	int T1303_o0;
	int T1303_o1;
	int T1303_W;

	int T1304_i0;
	int T1304_i1;
	int T1304_o0;
	int T1304_o1;
	int T1304_W;

	int T1305_i0;
	int T1305_i1;
	int T1305_o0;
	int T1305_o1;
	int T1305_W;

	int T1306_i0;
	int T1306_i1;
	int T1306_o0;
	int T1306_o1;
	int T1306_W;

	int T1307_i0;
	int T1307_i1;
	int T1307_o0;
	int T1307_o1;
	int T1307_W;

	int T1308_i0;
	int T1308_i1;
	int T1308_o0;
	int T1308_o1;
	int T1308_W;

	int T1309_i0;
	int T1309_i1;
	int T1309_o0;
	int T1309_o1;
	int T1309_W;

	int T1310_i0;
	int T1310_i1;
	int T1310_o0;
	int T1310_o1;
	int T1310_W;

	int T1311_i0;
	int T1311_i1;
	int T1311_o0;
	int T1311_o1;
	int T1311_W;

	int T1312_i0;
	int T1312_i1;
	int T1312_o0;
	int T1312_o1;
	int T1312_W;

	int T1313_i0;
	int T1313_i1;
	int T1313_o0;
	int T1313_o1;
	int T1313_W;

	int T1314_i0;
	int T1314_i1;
	int T1314_o0;
	int T1314_o1;
	int T1314_W;

	int T1315_i0;
	int T1315_i1;
	int T1315_o0;
	int T1315_o1;
	int T1315_W;

	int T1316_i0;
	int T1316_i1;
	int T1316_o0;
	int T1316_o1;
	int T1316_W;

	int T1317_i0;
	int T1317_i1;
	int T1317_o0;
	int T1317_o1;
	int T1317_W;

	int T1318_i0;
	int T1318_i1;
	int T1318_o0;
	int T1318_o1;
	int T1318_W;

	int T1319_i0;
	int T1319_i1;
	int T1319_o0;
	int T1319_o1;
	int T1319_W;

	int T1320_i0;
	int T1320_i1;
	int T1320_o0;
	int T1320_o1;
	int T1320_W;

	int T1321_i0;
	int T1321_i1;
	int T1321_o0;
	int T1321_o1;
	int T1321_W;

	int T1322_i0;
	int T1322_i1;
	int T1322_o0;
	int T1322_o1;
	int T1322_W;

	int T1323_i0;
	int T1323_i1;
	int T1323_o0;
	int T1323_o1;
	int T1323_W;

	int T1324_i0;
	int T1324_i1;
	int T1324_o0;
	int T1324_o1;
	int T1324_W;

	int T1325_i0;
	int T1325_i1;
	int T1325_o0;
	int T1325_o1;
	int T1325_W;

	int T1326_i0;
	int T1326_i1;
	int T1326_o0;
	int T1326_o1;
	int T1326_W;

	int T1327_i0;
	int T1327_i1;
	int T1327_o0;
	int T1327_o1;
	int T1327_W;

	int T1328_i0;
	int T1328_i1;
	int T1328_o0;
	int T1328_o1;
	int T1328_W;

	int T1329_i0;
	int T1329_i1;
	int T1329_o0;
	int T1329_o1;
	int T1329_W;

	int T1330_i0;
	int T1330_i1;
	int T1330_o0;
	int T1330_o1;
	int T1330_W;

	int T1331_i0;
	int T1331_i1;
	int T1331_o0;
	int T1331_o1;
	int T1331_W;

	int T1332_i0;
	int T1332_i1;
	int T1332_o0;
	int T1332_o1;
	int T1332_W;

	int T1333_i0;
	int T1333_i1;
	int T1333_o0;
	int T1333_o1;
	int T1333_W;

	int T1334_i0;
	int T1334_i1;
	int T1334_o0;
	int T1334_o1;
	int T1334_W;

	int T1335_i0;
	int T1335_i1;
	int T1335_o0;
	int T1335_o1;
	int T1335_W;

	int T1336_i0;
	int T1336_i1;
	int T1336_o0;
	int T1336_o1;
	int T1336_W;

	int T1337_i0;
	int T1337_i1;
	int T1337_o0;
	int T1337_o1;
	int T1337_W;

	int T1338_i0;
	int T1338_i1;
	int T1338_o0;
	int T1338_o1;
	int T1338_W;

	int T1339_i0;
	int T1339_i1;
	int T1339_o0;
	int T1339_o1;
	int T1339_W;

	int T1340_i0;
	int T1340_i1;
	int T1340_o0;
	int T1340_o1;
	int T1340_W;

	int T1341_i0;
	int T1341_i1;
	int T1341_o0;
	int T1341_o1;
	int T1341_W;

	int T1342_i0;
	int T1342_i1;
	int T1342_o0;
	int T1342_o1;
	int T1342_W;

	int T1343_i0;
	int T1343_i1;
	int T1343_o0;
	int T1343_o1;
	int T1343_W;

	int T1344_i0;
	int T1344_i1;
	int T1344_o0;
	int T1344_o1;
	int T1344_W;

	int T1345_i0;
	int T1345_i1;
	int T1345_o0;
	int T1345_o1;
	int T1345_W;

	int T1346_i0;
	int T1346_i1;
	int T1346_o0;
	int T1346_o1;
	int T1346_W;

	int T1347_i0;
	int T1347_i1;
	int T1347_o0;
	int T1347_o1;
	int T1347_W;

	int T1348_i0;
	int T1348_i1;
	int T1348_o0;
	int T1348_o1;
	int T1348_W;

	int T1349_i0;
	int T1349_i1;
	int T1349_o0;
	int T1349_o1;
	int T1349_W;

	int T1350_i0;
	int T1350_i1;
	int T1350_o0;
	int T1350_o1;
	int T1350_W;

	int T1351_i0;
	int T1351_i1;
	int T1351_o0;
	int T1351_o1;
	int T1351_W;

	int T1352_i0;
	int T1352_i1;
	int T1352_o0;
	int T1352_o1;
	int T1352_W;

	int T1353_i0;
	int T1353_i1;
	int T1353_o0;
	int T1353_o1;
	int T1353_W;

	int T1354_i0;
	int T1354_i1;
	int T1354_o0;
	int T1354_o1;
	int T1354_W;

	int T1355_i0;
	int T1355_i1;
	int T1355_o0;
	int T1355_o1;
	int T1355_W;

	int T1356_i0;
	int T1356_i1;
	int T1356_o0;
	int T1356_o1;
	int T1356_W;

	int T1357_i0;
	int T1357_i1;
	int T1357_o0;
	int T1357_o1;
	int T1357_W;

	int T1358_i0;
	int T1358_i1;
	int T1358_o0;
	int T1358_o1;
	int T1358_W;

	int T1359_i0;
	int T1359_i1;
	int T1359_o0;
	int T1359_o1;
	int T1359_W;

	int T1360_i0;
	int T1360_i1;
	int T1360_o0;
	int T1360_o1;
	int T1360_W;

	int T1361_i0;
	int T1361_i1;
	int T1361_o0;
	int T1361_o1;
	int T1361_W;

	int T1362_i0;
	int T1362_i1;
	int T1362_o0;
	int T1362_o1;
	int T1362_W;

	int T1363_i0;
	int T1363_i1;
	int T1363_o0;
	int T1363_o1;
	int T1363_W;

	int T1364_i0;
	int T1364_i1;
	int T1364_o0;
	int T1364_o1;
	int T1364_W;

	int T1365_i0;
	int T1365_i1;
	int T1365_o0;
	int T1365_o1;
	int T1365_W;

	int T1366_i0;
	int T1366_i1;
	int T1366_o0;
	int T1366_o1;
	int T1366_W;

	int T1367_i0;
	int T1367_i1;
	int T1367_o0;
	int T1367_o1;
	int T1367_W;

	int T1368_i0;
	int T1368_i1;
	int T1368_o0;
	int T1368_o1;
	int T1368_W;

	int T1369_i0;
	int T1369_i1;
	int T1369_o0;
	int T1369_o1;
	int T1369_W;

	int T1370_i0;
	int T1370_i1;
	int T1370_o0;
	int T1370_o1;
	int T1370_W;

	int T1371_i0;
	int T1371_i1;
	int T1371_o0;
	int T1371_o1;
	int T1371_W;

	int T1372_i0;
	int T1372_i1;
	int T1372_o0;
	int T1372_o1;
	int T1372_W;

	int T1373_i0;
	int T1373_i1;
	int T1373_o0;
	int T1373_o1;
	int T1373_W;

	int T1374_i0;
	int T1374_i1;
	int T1374_o0;
	int T1374_o1;
	int T1374_W;

	int T1375_i0;
	int T1375_i1;
	int T1375_o0;
	int T1375_o1;
	int T1375_W;

	int T1376_i0;
	int T1376_i1;
	int T1376_o0;
	int T1376_o1;
	int T1376_W;

	int T1377_i0;
	int T1377_i1;
	int T1377_o0;
	int T1377_o1;
	int T1377_W;

	int T1378_i0;
	int T1378_i1;
	int T1378_o0;
	int T1378_o1;
	int T1378_W;

	int T1379_i0;
	int T1379_i1;
	int T1379_o0;
	int T1379_o1;
	int T1379_W;

	int T1380_i0;
	int T1380_i1;
	int T1380_o0;
	int T1380_o1;
	int T1380_W;

	int T1381_i0;
	int T1381_i1;
	int T1381_o0;
	int T1381_o1;
	int T1381_W;

	int T1382_i0;
	int T1382_i1;
	int T1382_o0;
	int T1382_o1;
	int T1382_W;

	int T1383_i0;
	int T1383_i1;
	int T1383_o0;
	int T1383_o1;
	int T1383_W;

	int T1384_i0;
	int T1384_i1;
	int T1384_o0;
	int T1384_o1;
	int T1384_W;

	int T1385_i0;
	int T1385_i1;
	int T1385_o0;
	int T1385_o1;
	int T1385_W;

	int T1386_i0;
	int T1386_i1;
	int T1386_o0;
	int T1386_o1;
	int T1386_W;

	int T1387_i0;
	int T1387_i1;
	int T1387_o0;
	int T1387_o1;
	int T1387_W;

	int T1388_i0;
	int T1388_i1;
	int T1388_o0;
	int T1388_o1;
	int T1388_W;

	int T1389_i0;
	int T1389_i1;
	int T1389_o0;
	int T1389_o1;
	int T1389_W;

	int T1390_i0;
	int T1390_i1;
	int T1390_o0;
	int T1390_o1;
	int T1390_W;

	int T1391_i0;
	int T1391_i1;
	int T1391_o0;
	int T1391_o1;
	int T1391_W;

	int T1392_i0;
	int T1392_i1;
	int T1392_o0;
	int T1392_o1;
	int T1392_W;

	int T1393_i0;
	int T1393_i1;
	int T1393_o0;
	int T1393_o1;
	int T1393_W;

	int T1394_i0;
	int T1394_i1;
	int T1394_o0;
	int T1394_o1;
	int T1394_W;

	int T1395_i0;
	int T1395_i1;
	int T1395_o0;
	int T1395_o1;
	int T1395_W;

	int T1396_i0;
	int T1396_i1;
	int T1396_o0;
	int T1396_o1;
	int T1396_W;

	int T1397_i0;
	int T1397_i1;
	int T1397_o0;
	int T1397_o1;
	int T1397_W;

	int T1398_i0;
	int T1398_i1;
	int T1398_o0;
	int T1398_o1;
	int T1398_W;

	int T1399_i0;
	int T1399_i1;
	int T1399_o0;
	int T1399_o1;
	int T1399_W;

	int T1400_i0;
	int T1400_i1;
	int T1400_o0;
	int T1400_o1;
	int T1400_W;

	int T1401_i0;
	int T1401_i1;
	int T1401_o0;
	int T1401_o1;
	int T1401_W;

	int T1402_i0;
	int T1402_i1;
	int T1402_o0;
	int T1402_o1;
	int T1402_W;

	int T1403_i0;
	int T1403_i1;
	int T1403_o0;
	int T1403_o1;
	int T1403_W;

	int T1404_i0;
	int T1404_i1;
	int T1404_o0;
	int T1404_o1;
	int T1404_W;

	int T1405_i0;
	int T1405_i1;
	int T1405_o0;
	int T1405_o1;
	int T1405_W;

	int T1406_i0;
	int T1406_i1;
	int T1406_o0;
	int T1406_o1;
	int T1406_W;

	int T1407_i0;
	int T1407_i1;
	int T1407_o0;
	int T1407_o1;
	int T1407_W;

	int T1408_i0;
	int T1408_i1;
	int T1408_o0;
	int T1408_o1;
	int T1408_W;

	int T1409_i0;
	int T1409_i1;
	int T1409_o0;
	int T1409_o1;
	int T1409_W;

	int T1410_i0;
	int T1410_i1;
	int T1410_o0;
	int T1410_o1;
	int T1410_W;

	int T1411_i0;
	int T1411_i1;
	int T1411_o0;
	int T1411_o1;
	int T1411_W;

	int T1412_i0;
	int T1412_i1;
	int T1412_o0;
	int T1412_o1;
	int T1412_W;

	int T1413_i0;
	int T1413_i1;
	int T1413_o0;
	int T1413_o1;
	int T1413_W;

	int T1414_i0;
	int T1414_i1;
	int T1414_o0;
	int T1414_o1;
	int T1414_W;

	int T1415_i0;
	int T1415_i1;
	int T1415_o0;
	int T1415_o1;
	int T1415_W;

	int T1416_i0;
	int T1416_i1;
	int T1416_o0;
	int T1416_o1;
	int T1416_W;

	int T1417_i0;
	int T1417_i1;
	int T1417_o0;
	int T1417_o1;
	int T1417_W;

	int T1418_i0;
	int T1418_i1;
	int T1418_o0;
	int T1418_o1;
	int T1418_W;

	int T1419_i0;
	int T1419_i1;
	int T1419_o0;
	int T1419_o1;
	int T1419_W;

	int T1420_i0;
	int T1420_i1;
	int T1420_o0;
	int T1420_o1;
	int T1420_W;

	int T1421_i0;
	int T1421_i1;
	int T1421_o0;
	int T1421_o1;
	int T1421_W;

	int T1422_i0;
	int T1422_i1;
	int T1422_o0;
	int T1422_o1;
	int T1422_W;

	int T1423_i0;
	int T1423_i1;
	int T1423_o0;
	int T1423_o1;
	int T1423_W;

	int T1424_i0;
	int T1424_i1;
	int T1424_o0;
	int T1424_o1;
	int T1424_W;

	int T1425_i0;
	int T1425_i1;
	int T1425_o0;
	int T1425_o1;
	int T1425_W;

	int T1426_i0;
	int T1426_i1;
	int T1426_o0;
	int T1426_o1;
	int T1426_W;

	int T1427_i0;
	int T1427_i1;
	int T1427_o0;
	int T1427_o1;
	int T1427_W;

	int T1428_i0;
	int T1428_i1;
	int T1428_o0;
	int T1428_o1;
	int T1428_W;

	int T1429_i0;
	int T1429_i1;
	int T1429_o0;
	int T1429_o1;
	int T1429_W;

	int T1430_i0;
	int T1430_i1;
	int T1430_o0;
	int T1430_o1;
	int T1430_W;

	int T1431_i0;
	int T1431_i1;
	int T1431_o0;
	int T1431_o1;
	int T1431_W;

	int T1432_i0;
	int T1432_i1;
	int T1432_o0;
	int T1432_o1;
	int T1432_W;

	int T1433_i0;
	int T1433_i1;
	int T1433_o0;
	int T1433_o1;
	int T1433_W;

	int T1434_i0;
	int T1434_i1;
	int T1434_o0;
	int T1434_o1;
	int T1434_W;

	int T1435_i0;
	int T1435_i1;
	int T1435_o0;
	int T1435_o1;
	int T1435_W;

	int T1436_i0;
	int T1436_i1;
	int T1436_o0;
	int T1436_o1;
	int T1436_W;

	int T1437_i0;
	int T1437_i1;
	int T1437_o0;
	int T1437_o1;
	int T1437_W;

	int T1438_i0;
	int T1438_i1;
	int T1438_o0;
	int T1438_o1;
	int T1438_W;

	int T1439_i0;
	int T1439_i1;
	int T1439_o0;
	int T1439_o1;
	int T1439_W;

	int T1440_i0;
	int T1440_i1;
	int T1440_o0;
	int T1440_o1;
	int T1440_W;

	int T1441_i0;
	int T1441_i1;
	int T1441_o0;
	int T1441_o1;
	int T1441_W;

	int T1442_i0;
	int T1442_i1;
	int T1442_o0;
	int T1442_o1;
	int T1442_W;

	int T1443_i0;
	int T1443_i1;
	int T1443_o0;
	int T1443_o1;
	int T1443_W;

	int T1444_i0;
	int T1444_i1;
	int T1444_o0;
	int T1444_o1;
	int T1444_W;

	int T1445_i0;
	int T1445_i1;
	int T1445_o0;
	int T1445_o1;
	int T1445_W;

	int T1446_i0;
	int T1446_i1;
	int T1446_o0;
	int T1446_o1;
	int T1446_W;

	int T1447_i0;
	int T1447_i1;
	int T1447_o0;
	int T1447_o1;
	int T1447_W;

	int T1448_i0;
	int T1448_i1;
	int T1448_o0;
	int T1448_o1;
	int T1448_W;

	int T1449_i0;
	int T1449_i1;
	int T1449_o0;
	int T1449_o1;
	int T1449_W;

	int T1450_i0;
	int T1450_i1;
	int T1450_o0;
	int T1450_o1;
	int T1450_W;

	int T1451_i0;
	int T1451_i1;
	int T1451_o0;
	int T1451_o1;
	int T1451_W;

	int T1452_i0;
	int T1452_i1;
	int T1452_o0;
	int T1452_o1;
	int T1452_W;

	int T1453_i0;
	int T1453_i1;
	int T1453_o0;
	int T1453_o1;
	int T1453_W;

	int T1454_i0;
	int T1454_i1;
	int T1454_o0;
	int T1454_o1;
	int T1454_W;

	int T1455_i0;
	int T1455_i1;
	int T1455_o0;
	int T1455_o1;
	int T1455_W;

	int T1456_i0;
	int T1456_i1;
	int T1456_o0;
	int T1456_o1;
	int T1456_W;

	int T1457_i0;
	int T1457_i1;
	int T1457_o0;
	int T1457_o1;
	int T1457_W;

	int T1458_i0;
	int T1458_i1;
	int T1458_o0;
	int T1458_o1;
	int T1458_W;

	int T1459_i0;
	int T1459_i1;
	int T1459_o0;
	int T1459_o1;
	int T1459_W;

	int T1460_i0;
	int T1460_i1;
	int T1460_o0;
	int T1460_o1;
	int T1460_W;

	int T1461_i0;
	int T1461_i1;
	int T1461_o0;
	int T1461_o1;
	int T1461_W;

	int T1462_i0;
	int T1462_i1;
	int T1462_o0;
	int T1462_o1;
	int T1462_W;

	int T1463_i0;
	int T1463_i1;
	int T1463_o0;
	int T1463_o1;
	int T1463_W;

	int T1464_i0;
	int T1464_i1;
	int T1464_o0;
	int T1464_o1;
	int T1464_W;

	int T1465_i0;
	int T1465_i1;
	int T1465_o0;
	int T1465_o1;
	int T1465_W;

	int T1466_i0;
	int T1466_i1;
	int T1466_o0;
	int T1466_o1;
	int T1466_W;

	int T1467_i0;
	int T1467_i1;
	int T1467_o0;
	int T1467_o1;
	int T1467_W;

	int T1468_i0;
	int T1468_i1;
	int T1468_o0;
	int T1468_o1;
	int T1468_W;

	int T1469_i0;
	int T1469_i1;
	int T1469_o0;
	int T1469_o1;
	int T1469_W;

	int T1470_i0;
	int T1470_i1;
	int T1470_o0;
	int T1470_o1;
	int T1470_W;

	int T1471_i0;
	int T1471_i1;
	int T1471_o0;
	int T1471_o1;
	int T1471_W;

	int T1472_i0;
	int T1472_i1;
	int T1472_o0;
	int T1472_o1;
	int T1472_W;

	int T1473_i0;
	int T1473_i1;
	int T1473_o0;
	int T1473_o1;
	int T1473_W;

	int T1474_i0;
	int T1474_i1;
	int T1474_o0;
	int T1474_o1;
	int T1474_W;

	int T1475_i0;
	int T1475_i1;
	int T1475_o0;
	int T1475_o1;
	int T1475_W;

	int T1476_i0;
	int T1476_i1;
	int T1476_o0;
	int T1476_o1;
	int T1476_W;

	int T1477_i0;
	int T1477_i1;
	int T1477_o0;
	int T1477_o1;
	int T1477_W;

	int T1478_i0;
	int T1478_i1;
	int T1478_o0;
	int T1478_o1;
	int T1478_W;

	int T1479_i0;
	int T1479_i1;
	int T1479_o0;
	int T1479_o1;
	int T1479_W;

	int T1480_i0;
	int T1480_i1;
	int T1480_o0;
	int T1480_o1;
	int T1480_W;

	int T1481_i0;
	int T1481_i1;
	int T1481_o0;
	int T1481_o1;
	int T1481_W;

	int T1482_i0;
	int T1482_i1;
	int T1482_o0;
	int T1482_o1;
	int T1482_W;

	int T1483_i0;
	int T1483_i1;
	int T1483_o0;
	int T1483_o1;
	int T1483_W;

	int T1484_i0;
	int T1484_i1;
	int T1484_o0;
	int T1484_o1;
	int T1484_W;

	int T1485_i0;
	int T1485_i1;
	int T1485_o0;
	int T1485_o1;
	int T1485_W;

	int T1486_i0;
	int T1486_i1;
	int T1486_o0;
	int T1486_o1;
	int T1486_W;

	int T1487_i0;
	int T1487_i1;
	int T1487_o0;
	int T1487_o1;
	int T1487_W;

	int T1488_i0;
	int T1488_i1;
	int T1488_o0;
	int T1488_o1;
	int T1488_W;

	int T1489_i0;
	int T1489_i1;
	int T1489_o0;
	int T1489_o1;
	int T1489_W;

	int T1490_i0;
	int T1490_i1;
	int T1490_o0;
	int T1490_o1;
	int T1490_W;

	int T1491_i0;
	int T1491_i1;
	int T1491_o0;
	int T1491_o1;
	int T1491_W;

	int T1492_i0;
	int T1492_i1;
	int T1492_o0;
	int T1492_o1;
	int T1492_W;

	int T1493_i0;
	int T1493_i1;
	int T1493_o0;
	int T1493_o1;
	int T1493_W;

	int T1494_i0;
	int T1494_i1;
	int T1494_o0;
	int T1494_o1;
	int T1494_W;

	int T1495_i0;
	int T1495_i1;
	int T1495_o0;
	int T1495_o1;
	int T1495_W;

	int T1496_i0;
	int T1496_i1;
	int T1496_o0;
	int T1496_o1;
	int T1496_W;

	int T1497_i0;
	int T1497_i1;
	int T1497_o0;
	int T1497_o1;
	int T1497_W;

	int T1498_i0;
	int T1498_i1;
	int T1498_o0;
	int T1498_o1;
	int T1498_W;

	int T1499_i0;
	int T1499_i1;
	int T1499_o0;
	int T1499_o1;
	int T1499_W;

	int T1500_i0;
	int T1500_i1;
	int T1500_o0;
	int T1500_o1;
	int T1500_W;

	int T1501_i0;
	int T1501_i1;
	int T1501_o0;
	int T1501_o1;
	int T1501_W;

	int T1502_i0;
	int T1502_i1;
	int T1502_o0;
	int T1502_o1;
	int T1502_W;

	int T1503_i0;
	int T1503_i1;
	int T1503_o0;
	int T1503_o1;
	int T1503_W;

	int T1504_i0;
	int T1504_i1;
	int T1504_o0;
	int T1504_o1;
	int T1504_W;

	int T1505_i0;
	int T1505_i1;
	int T1505_o0;
	int T1505_o1;
	int T1505_W;

	int T1506_i0;
	int T1506_i1;
	int T1506_o0;
	int T1506_o1;
	int T1506_W;

	int T1507_i0;
	int T1507_i1;
	int T1507_o0;
	int T1507_o1;
	int T1507_W;

	int T1508_i0;
	int T1508_i1;
	int T1508_o0;
	int T1508_o1;
	int T1508_W;

	int T1509_i0;
	int T1509_i1;
	int T1509_o0;
	int T1509_o1;
	int T1509_W;

	int T1510_i0;
	int T1510_i1;
	int T1510_o0;
	int T1510_o1;
	int T1510_W;

	int T1511_i0;
	int T1511_i1;
	int T1511_o0;
	int T1511_o1;
	int T1511_W;

	int T1512_i0;
	int T1512_i1;
	int T1512_o0;
	int T1512_o1;
	int T1512_W;

	int T1513_i0;
	int T1513_i1;
	int T1513_o0;
	int T1513_o1;
	int T1513_W;

	int T1514_i0;
	int T1514_i1;
	int T1514_o0;
	int T1514_o1;
	int T1514_W;

	int T1515_i0;
	int T1515_i1;
	int T1515_o0;
	int T1515_o1;
	int T1515_W;

	int T1516_i0;
	int T1516_i1;
	int T1516_o0;
	int T1516_o1;
	int T1516_W;

	int T1517_i0;
	int T1517_i1;
	int T1517_o0;
	int T1517_o1;
	int T1517_W;

	int T1518_i0;
	int T1518_i1;
	int T1518_o0;
	int T1518_o1;
	int T1518_W;

	int T1519_i0;
	int T1519_i1;
	int T1519_o0;
	int T1519_o1;
	int T1519_W;

	int T1520_i0;
	int T1520_i1;
	int T1520_o0;
	int T1520_o1;
	int T1520_W;

	int T1521_i0;
	int T1521_i1;
	int T1521_o0;
	int T1521_o1;
	int T1521_W;

	int T1522_i0;
	int T1522_i1;
	int T1522_o0;
	int T1522_o1;
	int T1522_W;

	int T1523_i0;
	int T1523_i1;
	int T1523_o0;
	int T1523_o1;
	int T1523_W;

	int T1524_i0;
	int T1524_i1;
	int T1524_o0;
	int T1524_o1;
	int T1524_W;

	int T1525_i0;
	int T1525_i1;
	int T1525_o0;
	int T1525_o1;
	int T1525_W;

	int T1526_i0;
	int T1526_i1;
	int T1526_o0;
	int T1526_o1;
	int T1526_W;

	int T1527_i0;
	int T1527_i1;
	int T1527_o0;
	int T1527_o1;
	int T1527_W;

	int T1528_i0;
	int T1528_i1;
	int T1528_o0;
	int T1528_o1;
	int T1528_W;

	int T1529_i0;
	int T1529_i1;
	int T1529_o0;
	int T1529_o1;
	int T1529_W;

	int T1530_i0;
	int T1530_i1;
	int T1530_o0;
	int T1530_o1;
	int T1530_W;

	int T1531_i0;
	int T1531_i1;
	int T1531_o0;
	int T1531_o1;
	int T1531_W;

	int T1532_i0;
	int T1532_i1;
	int T1532_o0;
	int T1532_o1;
	int T1532_W;

	int T1533_i0;
	int T1533_i1;
	int T1533_o0;
	int T1533_o1;
	int T1533_W;

	int T1534_i0;
	int T1534_i1;
	int T1534_o0;
	int T1534_o1;
	int T1534_W;

	int T1535_i0;
	int T1535_i1;
	int T1535_o0;
	int T1535_o1;
	int T1535_W;


  // **** Parameter initialisation **** //
T1280_W = 16384;
T1281_W = -105234511;
T1282_W = -209436987;
T1283_W = -311673537;
T1284_W = -410895583;
T1285_W = -506120079;
T1286_W = -596495049;
T1287_W = -681168519;
T1288_W = -759222975;
T1289_W = -830003046;
T1290_W = -892787826;
T1291_W = -946921941;
T1292_W = -992012162;
T1293_W = -1027534188;
T1294_W = -1053094788;
T1295_W = -1068562874;
T1296_W = -1073741824;
T1297_W = -1068566086;
T1298_W = -1053101180;
T1299_W = -1027543700;
T1300_W = -992024702;
T1301_W = -946937387;
T1302_W = -892806030;
T1303_W = -830023834;
T1304_W = -759246145;
T1305_W = -681193849;
T1306_W = -596522295;
T1307_W = -506148977;
T1308_W = -410925857;
T1309_W = -311704895;
T1310_W = -209469125;
T1311_W = -105267121;
T1312_W = 16384;
T1313_W = -105234511;
T1314_W = -209436987;
T1315_W = -311673537;
T1316_W = -410895583;
T1317_W = -506120079;
T1318_W = -596495049;
T1319_W = -681168519;
T1320_W = -759222975;
T1321_W = -830003046;
T1322_W = -892787826;
T1323_W = -946921941;
T1324_W = -992012162;
T1325_W = -1027534188;
T1326_W = -1053094788;
T1327_W = -1068562874;
T1328_W = -1073741824;
T1329_W = -1068566086;
T1330_W = -1053101180;
T1331_W = -1027543700;
T1332_W = -992024702;
T1333_W = -946937387;
T1334_W = -892806030;
T1335_W = -830023834;
T1336_W = -759246145;
T1337_W = -681193849;
T1338_W = -596522295;
T1339_W = -506148977;
T1340_W = -410925857;
T1341_W = -311704895;
T1342_W = -209469125;
T1343_W = -105267121;
T1344_W = 16384;
T1345_W = -105234511;
T1346_W = -209436987;
T1347_W = -311673537;
T1348_W = -410895583;
T1349_W = -506120079;
T1350_W = -596495049;
T1351_W = -681168519;
T1352_W = -759222975;
T1353_W = -830003046;
T1354_W = -892787826;
T1355_W = -946921941;
T1356_W = -992012162;
T1357_W = -1027534188;
T1358_W = -1053094788;
T1359_W = -1068562874;
T1360_W = -1073741824;
T1361_W = -1068566086;
T1362_W = -1053101180;
T1363_W = -1027543700;
T1364_W = -992024702;
T1365_W = -946937387;
T1366_W = -892806030;
T1367_W = -830023834;
T1368_W = -759246145;
T1369_W = -681193849;
T1370_W = -596522295;
T1371_W = -506148977;
T1372_W = -410925857;
T1373_W = -311704895;
T1374_W = -209469125;
T1375_W = -105267121;
T1376_W = 16384;
T1377_W = -105234511;
T1378_W = -209436987;
T1379_W = -311673537;
T1380_W = -410895583;
T1381_W = -506120079;
T1382_W = -596495049;
T1383_W = -681168519;
T1384_W = -759222975;
T1385_W = -830003046;
T1386_W = -892787826;
T1387_W = -946921941;
T1388_W = -992012162;
T1389_W = -1027534188;
T1390_W = -1053094788;
T1391_W = -1068562874;
T1392_W = -1073741824;
T1393_W = -1068566086;
T1394_W = -1053101180;
T1395_W = -1027543700;
T1396_W = -992024702;
T1397_W = -946937387;
T1398_W = -892806030;
T1399_W = -830023834;
T1400_W = -759246145;
T1401_W = -681193849;
T1402_W = -596522295;
T1403_W = -506148977;
T1404_W = -410925857;
T1405_W = -311704895;
T1406_W = -209469125;
T1407_W = -105267121;
T1408_W = 16384;
T1409_W = -105234511;
T1410_W = -209436987;
T1411_W = -311673537;
T1412_W = -410895583;
T1413_W = -506120079;
T1414_W = -596495049;
T1415_W = -681168519;
T1416_W = -759222975;
T1417_W = -830003046;
T1418_W = -892787826;
T1419_W = -946921941;
T1420_W = -992012162;
T1421_W = -1027534188;
T1422_W = -1053094788;
T1423_W = -1068562874;
T1424_W = -1073741824;
T1425_W = -1068566086;
T1426_W = -1053101180;
T1427_W = -1027543700;
T1428_W = -992024702;
T1429_W = -946937387;
T1430_W = -892806030;
T1431_W = -830023834;
T1432_W = -759246145;
T1433_W = -681193849;
T1434_W = -596522295;
T1435_W = -506148977;
T1436_W = -410925857;
T1437_W = -311704895;
T1438_W = -209469125;
T1439_W = -105267121;
T1440_W = 16384;
T1441_W = -105234511;
T1442_W = -209436987;
T1443_W = -311673537;
T1444_W = -410895583;
T1445_W = -506120079;
T1446_W = -596495049;
T1447_W = -681168519;
T1448_W = -759222975;
T1449_W = -830003046;
T1450_W = -892787826;
T1451_W = -946921941;
T1452_W = -992012162;
T1453_W = -1027534188;
T1454_W = -1053094788;
T1455_W = -1068562874;
T1456_W = -1073741824;
T1457_W = -1068566086;
T1458_W = -1053101180;
T1459_W = -1027543700;
T1460_W = -992024702;
T1461_W = -946937387;
T1462_W = -892806030;
T1463_W = -830023834;
T1464_W = -759246145;
T1465_W = -681193849;
T1466_W = -596522295;
T1467_W = -506148977;
T1468_W = -410925857;
T1469_W = -311704895;
T1470_W = -209469125;
T1471_W = -105267121;
T1472_W = 16384;
T1473_W = -105234511;
T1474_W = -209436987;
T1475_W = -311673537;
T1476_W = -410895583;
T1477_W = -506120079;
T1478_W = -596495049;
T1479_W = -681168519;
T1480_W = -759222975;
T1481_W = -830003046;
T1482_W = -892787826;
T1483_W = -946921941;
T1484_W = -992012162;
T1485_W = -1027534188;
T1486_W = -1053094788;
T1487_W = -1068562874;
T1488_W = -1073741824;
T1489_W = -1068566086;
T1490_W = -1053101180;
T1491_W = -1027543700;
T1492_W = -992024702;
T1493_W = -946937387;
T1494_W = -892806030;
T1495_W = -830023834;
T1496_W = -759246145;
T1497_W = -681193849;
T1498_W = -596522295;
T1499_W = -506148977;
T1500_W = -410925857;
T1501_W = -311704895;
T1502_W = -209469125;
T1503_W = -105267121;
T1504_W = 16384;
T1505_W = -105234511;
T1506_W = -209436987;
T1507_W = -311673537;
T1508_W = -410895583;
T1509_W = -506120079;
T1510_W = -596495049;
T1511_W = -681168519;
T1512_W = -759222975;
T1513_W = -830003046;
T1514_W = -892787826;
T1515_W = -946921941;
T1516_W = -992012162;
T1517_W = -1027534188;
T1518_W = -1053094788;
T1519_W = -1068562874;
T1520_W = -1073741824;
T1521_W = -1068566086;
T1522_W = -1053101180;
T1523_W = -1027543700;
T1524_W = -992024702;
T1525_W = -946937387;
T1526_W = -892806030;
T1527_W = -830023834;
T1528_W = -759246145;
T1529_W = -681193849;
T1530_W = -596522295;
T1531_W = -506148977;
T1532_W = -410925857;
T1533_W = -311704895;
T1534_W = -209469125;
T1535_W = -105267121;

  // **** Code body **** //

	GET_FIFO(T1280_i0, 0);
	GET_FIFO(T1280_i1, 2);
	Butterfly(T1280_i0, T1280_i1, &T1280_o0, &T1280_o1, T1280_W);
	PUT_FIFO(T1280_o0, 0);
	PUT_FIFO(T1280_o1, 1);

	GET_FIFO(T1281_i0, 0);
	GET_FIFO(T1281_i1, 2);
	Butterfly(T1281_i0, T1281_i1, &T1281_o0, &T1281_o1, T1281_W);
	PUT_FIFO(T1281_o0, 0);
	PUT_FIFO(T1281_o1, 1);

	GET_FIFO(T1282_i0, 0);
	GET_FIFO(T1282_i1, 2);
	Butterfly(T1282_i0, T1282_i1, &T1282_o0, &T1282_o1, T1282_W);
	PUT_FIFO(T1282_o0, 0);
	PUT_FIFO(T1282_o1, 1);

	GET_FIFO(T1283_i0, 0);
	GET_FIFO(T1283_i1, 2);
	Butterfly(T1283_i0, T1283_i1, &T1283_o0, &T1283_o1, T1283_W);
	PUT_FIFO(T1283_o0, 0);
	PUT_FIFO(T1283_o1, 1);

	GET_FIFO(T1284_i0, 0);
	GET_FIFO(T1284_i1, 2);
	Butterfly(T1284_i0, T1284_i1, &T1284_o0, &T1284_o1, T1284_W);
	PUT_FIFO(T1284_o0, 0);
	PUT_FIFO(T1284_o1, 1);

	GET_FIFO(T1285_i0, 0);
	GET_FIFO(T1285_i1, 2);
	Butterfly(T1285_i0, T1285_i1, &T1285_o0, &T1285_o1, T1285_W);
	PUT_FIFO(T1285_o0, 0);
	PUT_FIFO(T1285_o1, 1);

	GET_FIFO(T1286_i0, 0);
	GET_FIFO(T1286_i1, 2);
	Butterfly(T1286_i0, T1286_i1, &T1286_o0, &T1286_o1, T1286_W);
	PUT_FIFO(T1286_o0, 0);
	PUT_FIFO(T1286_o1, 1);

	GET_FIFO(T1287_i0, 0);
	GET_FIFO(T1287_i1, 2);
	Butterfly(T1287_i0, T1287_i1, &T1287_o0, &T1287_o1, T1287_W);
	PUT_FIFO(T1287_o0, 0);
	PUT_FIFO(T1287_o1, 1);

	GET_FIFO(T1288_i0, 0);
	GET_FIFO(T1288_i1, 2);
	Butterfly(T1288_i0, T1288_i1, &T1288_o0, &T1288_o1, T1288_W);
	PUT_FIFO(T1288_o0, 0);
	PUT_FIFO(T1288_o1, 1);

	GET_FIFO(T1289_i0, 0);
	GET_FIFO(T1289_i1, 2);
	Butterfly(T1289_i0, T1289_i1, &T1289_o0, &T1289_o1, T1289_W);
	PUT_FIFO(T1289_o0, 0);
	PUT_FIFO(T1289_o1, 1);

	GET_FIFO(T1290_i0, 0);
	GET_FIFO(T1290_i1, 2);
	Butterfly(T1290_i0, T1290_i1, &T1290_o0, &T1290_o1, T1290_W);
	PUT_FIFO(T1290_o0, 0);
	PUT_FIFO(T1290_o1, 1);

	GET_FIFO(T1291_i0, 0);
	GET_FIFO(T1291_i1, 2);
	Butterfly(T1291_i0, T1291_i1, &T1291_o0, &T1291_o1, T1291_W);
	PUT_FIFO(T1291_o0, 0);
	PUT_FIFO(T1291_o1, 1);

	GET_FIFO(T1292_i0, 0);
	GET_FIFO(T1292_i1, 2);
	Butterfly(T1292_i0, T1292_i1, &T1292_o0, &T1292_o1, T1292_W);
	PUT_FIFO(T1292_o0, 0);
	PUT_FIFO(T1292_o1, 1);

	GET_FIFO(T1293_i0, 0);
	GET_FIFO(T1293_i1, 2);
	Butterfly(T1293_i0, T1293_i1, &T1293_o0, &T1293_o1, T1293_W);
	PUT_FIFO(T1293_o0, 0);
	PUT_FIFO(T1293_o1, 1);

	GET_FIFO(T1294_i0, 0);
	GET_FIFO(T1294_i1, 2);
	Butterfly(T1294_i0, T1294_i1, &T1294_o0, &T1294_o1, T1294_W);
	PUT_FIFO(T1294_o0, 0);
	PUT_FIFO(T1294_o1, 1);

	GET_FIFO(T1295_i0, 0);
	GET_FIFO(T1295_i1, 2);
	Butterfly(T1295_i0, T1295_i1, &T1295_o0, &T1295_o1, T1295_W);
	PUT_FIFO(T1295_o0, 0);
	PUT_FIFO(T1295_o1, 1);

	GET_FIFO(T1296_i0, 1);
	GET_FIFO(T1296_i1, 3);
	Butterfly(T1296_i0, T1296_i1, &T1296_o0, &T1296_o1, T1296_W);
	PUT_FIFO(T1296_o0, 0);
	PUT_FIFO(T1296_o1, 1);

	GET_FIFO(T1297_i0, 1);
	GET_FIFO(T1297_i1, 3);
	Butterfly(T1297_i0, T1297_i1, &T1297_o0, &T1297_o1, T1297_W);
	PUT_FIFO(T1297_o0, 0);
	PUT_FIFO(T1297_o1, 1);

	GET_FIFO(T1298_i0, 1);
	GET_FIFO(T1298_i1, 3);
	Butterfly(T1298_i0, T1298_i1, &T1298_o0, &T1298_o1, T1298_W);
	PUT_FIFO(T1298_o0, 0);
	PUT_FIFO(T1298_o1, 1);

	GET_FIFO(T1299_i0, 1);
	GET_FIFO(T1299_i1, 3);
	Butterfly(T1299_i0, T1299_i1, &T1299_o0, &T1299_o1, T1299_W);
	PUT_FIFO(T1299_o0, 0);
	PUT_FIFO(T1299_o1, 1);

	GET_FIFO(T1300_i0, 1);
	GET_FIFO(T1300_i1, 3);
	Butterfly(T1300_i0, T1300_i1, &T1300_o0, &T1300_o1, T1300_W);
	PUT_FIFO(T1300_o0, 0);
	PUT_FIFO(T1300_o1, 1);

	GET_FIFO(T1301_i0, 1);
	GET_FIFO(T1301_i1, 3);
	Butterfly(T1301_i0, T1301_i1, &T1301_o0, &T1301_o1, T1301_W);
	PUT_FIFO(T1301_o0, 0);
	PUT_FIFO(T1301_o1, 1);

	GET_FIFO(T1302_i0, 1);
	GET_FIFO(T1302_i1, 3);
	Butterfly(T1302_i0, T1302_i1, &T1302_o0, &T1302_o1, T1302_W);
	PUT_FIFO(T1302_o0, 0);
	PUT_FIFO(T1302_o1, 1);

	GET_FIFO(T1303_i0, 1);
	GET_FIFO(T1303_i1, 3);
	Butterfly(T1303_i0, T1303_i1, &T1303_o0, &T1303_o1, T1303_W);
	PUT_FIFO(T1303_o0, 0);
	PUT_FIFO(T1303_o1, 1);

	GET_FIFO(T1304_i0, 1);
	GET_FIFO(T1304_i1, 3);
	Butterfly(T1304_i0, T1304_i1, &T1304_o0, &T1304_o1, T1304_W);
	PUT_FIFO(T1304_o0, 0);
	PUT_FIFO(T1304_o1, 1);

	GET_FIFO(T1305_i0, 1);
	GET_FIFO(T1305_i1, 3);
	Butterfly(T1305_i0, T1305_i1, &T1305_o0, &T1305_o1, T1305_W);
	PUT_FIFO(T1305_o0, 0);
	PUT_FIFO(T1305_o1, 1);

	GET_FIFO(T1306_i0, 1);
	GET_FIFO(T1306_i1, 3);
	Butterfly(T1306_i0, T1306_i1, &T1306_o0, &T1306_o1, T1306_W);
	PUT_FIFO(T1306_o0, 0);
	PUT_FIFO(T1306_o1, 1);

	GET_FIFO(T1307_i0, 1);
	GET_FIFO(T1307_i1, 3);
	Butterfly(T1307_i0, T1307_i1, &T1307_o0, &T1307_o1, T1307_W);
	PUT_FIFO(T1307_o0, 0);
	PUT_FIFO(T1307_o1, 1);

	GET_FIFO(T1308_i0, 1);
	GET_FIFO(T1308_i1, 3);
	Butterfly(T1308_i0, T1308_i1, &T1308_o0, &T1308_o1, T1308_W);
	PUT_FIFO(T1308_o0, 0);
	PUT_FIFO(T1308_o1, 1);

	GET_FIFO(T1309_i0, 1);
	GET_FIFO(T1309_i1, 3);
	Butterfly(T1309_i0, T1309_i1, &T1309_o0, &T1309_o1, T1309_W);
	PUT_FIFO(T1309_o0, 0);
	PUT_FIFO(T1309_o1, 1);

	GET_FIFO(T1310_i0, 1);
	GET_FIFO(T1310_i1, 3);
	Butterfly(T1310_i0, T1310_i1, &T1310_o0, &T1310_o1, T1310_W);
	PUT_FIFO(T1310_o0, 0);
	PUT_FIFO(T1310_o1, 1);

	GET_FIFO(T1311_i0, 1);
	GET_FIFO(T1311_i1, 3);
	Butterfly(T1311_i0, T1311_i1, &T1311_o0, &T1311_o1, T1311_W);
	PUT_FIFO(T1311_o0, 0);
	PUT_FIFO(T1311_o1, 1);

	GET_FIFO(T1312_i0, 0);
	GET_FIFO(T1312_i1, 2);
	Butterfly(T1312_i0, T1312_i1, &T1312_o0, &T1312_o1, T1312_W);
	PUT_FIFO(T1312_o0, 2);
	PUT_FIFO(T1312_o1, 3);

	GET_FIFO(T1313_i0, 0);
	GET_FIFO(T1313_i1, 2);
	Butterfly(T1313_i0, T1313_i1, &T1313_o0, &T1313_o1, T1313_W);
	PUT_FIFO(T1313_o0, 2);
	PUT_FIFO(T1313_o1, 3);

	GET_FIFO(T1314_i0, 0);
	GET_FIFO(T1314_i1, 2);
	Butterfly(T1314_i0, T1314_i1, &T1314_o0, &T1314_o1, T1314_W);
	PUT_FIFO(T1314_o0, 2);
	PUT_FIFO(T1314_o1, 3);

	GET_FIFO(T1315_i0, 0);
	GET_FIFO(T1315_i1, 2);
	Butterfly(T1315_i0, T1315_i1, &T1315_o0, &T1315_o1, T1315_W);
	PUT_FIFO(T1315_o0, 2);
	PUT_FIFO(T1315_o1, 3);

	GET_FIFO(T1316_i0, 0);
	GET_FIFO(T1316_i1, 2);
	Butterfly(T1316_i0, T1316_i1, &T1316_o0, &T1316_o1, T1316_W);
	PUT_FIFO(T1316_o0, 2);
	PUT_FIFO(T1316_o1, 3);

	GET_FIFO(T1317_i0, 0);
	GET_FIFO(T1317_i1, 2);
	Butterfly(T1317_i0, T1317_i1, &T1317_o0, &T1317_o1, T1317_W);
	PUT_FIFO(T1317_o0, 2);
	PUT_FIFO(T1317_o1, 3);

	GET_FIFO(T1318_i0, 0);
	GET_FIFO(T1318_i1, 2);
	Butterfly(T1318_i0, T1318_i1, &T1318_o0, &T1318_o1, T1318_W);
	PUT_FIFO(T1318_o0, 2);
	PUT_FIFO(T1318_o1, 3);

	GET_FIFO(T1319_i0, 0);
	GET_FIFO(T1319_i1, 2);
	Butterfly(T1319_i0, T1319_i1, &T1319_o0, &T1319_o1, T1319_W);
	PUT_FIFO(T1319_o0, 2);
	PUT_FIFO(T1319_o1, 3);

	GET_FIFO(T1320_i0, 0);
	GET_FIFO(T1320_i1, 2);
	Butterfly(T1320_i0, T1320_i1, &T1320_o0, &T1320_o1, T1320_W);
	PUT_FIFO(T1320_o0, 2);
	PUT_FIFO(T1320_o1, 3);

	GET_FIFO(T1321_i0, 0);
	GET_FIFO(T1321_i1, 2);
	Butterfly(T1321_i0, T1321_i1, &T1321_o0, &T1321_o1, T1321_W);
	PUT_FIFO(T1321_o0, 2);
	PUT_FIFO(T1321_o1, 3);

	GET_FIFO(T1322_i0, 0);
	GET_FIFO(T1322_i1, 2);
	Butterfly(T1322_i0, T1322_i1, &T1322_o0, &T1322_o1, T1322_W);
	PUT_FIFO(T1322_o0, 2);
	PUT_FIFO(T1322_o1, 3);

	GET_FIFO(T1323_i0, 0);
	GET_FIFO(T1323_i1, 2);
	Butterfly(T1323_i0, T1323_i1, &T1323_o0, &T1323_o1, T1323_W);
	PUT_FIFO(T1323_o0, 2);
	PUT_FIFO(T1323_o1, 3);

	GET_FIFO(T1324_i0, 0);
	GET_FIFO(T1324_i1, 2);
	Butterfly(T1324_i0, T1324_i1, &T1324_o0, &T1324_o1, T1324_W);
	PUT_FIFO(T1324_o0, 2);
	PUT_FIFO(T1324_o1, 3);

	GET_FIFO(T1325_i0, 0);
	GET_FIFO(T1325_i1, 2);
	Butterfly(T1325_i0, T1325_i1, &T1325_o0, &T1325_o1, T1325_W);
	PUT_FIFO(T1325_o0, 2);
	PUT_FIFO(T1325_o1, 3);

	GET_FIFO(T1326_i0, 0);
	GET_FIFO(T1326_i1, 2);
	Butterfly(T1326_i0, T1326_i1, &T1326_o0, &T1326_o1, T1326_W);
	PUT_FIFO(T1326_o0, 2);
	PUT_FIFO(T1326_o1, 3);

	GET_FIFO(T1327_i0, 0);
	GET_FIFO(T1327_i1, 2);
	Butterfly(T1327_i0, T1327_i1, &T1327_o0, &T1327_o1, T1327_W);
	PUT_FIFO(T1327_o0, 2);
	PUT_FIFO(T1327_o1, 3);

	GET_FIFO(T1328_i0, 1);
	GET_FIFO(T1328_i1, 3);
	Butterfly(T1328_i0, T1328_i1, &T1328_o0, &T1328_o1, T1328_W);
	PUT_FIFO(T1328_o0, 2);
	PUT_FIFO(T1328_o1, 3);

	GET_FIFO(T1329_i0, 1);
	GET_FIFO(T1329_i1, 3);
	Butterfly(T1329_i0, T1329_i1, &T1329_o0, &T1329_o1, T1329_W);
	PUT_FIFO(T1329_o0, 2);
	PUT_FIFO(T1329_o1, 3);

	GET_FIFO(T1330_i0, 1);
	GET_FIFO(T1330_i1, 3);
	Butterfly(T1330_i0, T1330_i1, &T1330_o0, &T1330_o1, T1330_W);
	PUT_FIFO(T1330_o0, 2);
	PUT_FIFO(T1330_o1, 3);

	GET_FIFO(T1331_i0, 1);
	GET_FIFO(T1331_i1, 3);
	Butterfly(T1331_i0, T1331_i1, &T1331_o0, &T1331_o1, T1331_W);
	PUT_FIFO(T1331_o0, 2);
	PUT_FIFO(T1331_o1, 3);

	GET_FIFO(T1332_i0, 1);
	GET_FIFO(T1332_i1, 3);
	Butterfly(T1332_i0, T1332_i1, &T1332_o0, &T1332_o1, T1332_W);
	PUT_FIFO(T1332_o0, 2);
	PUT_FIFO(T1332_o1, 3);

	GET_FIFO(T1333_i0, 1);
	GET_FIFO(T1333_i1, 3);
	Butterfly(T1333_i0, T1333_i1, &T1333_o0, &T1333_o1, T1333_W);
	PUT_FIFO(T1333_o0, 2);
	PUT_FIFO(T1333_o1, 3);

	GET_FIFO(T1334_i0, 1);
	GET_FIFO(T1334_i1, 3);
	Butterfly(T1334_i0, T1334_i1, &T1334_o0, &T1334_o1, T1334_W);
	PUT_FIFO(T1334_o0, 2);
	PUT_FIFO(T1334_o1, 3);

	GET_FIFO(T1335_i0, 1);
	GET_FIFO(T1335_i1, 3);
	Butterfly(T1335_i0, T1335_i1, &T1335_o0, &T1335_o1, T1335_W);
	PUT_FIFO(T1335_o0, 2);
	PUT_FIFO(T1335_o1, 3);

	GET_FIFO(T1336_i0, 1);
	GET_FIFO(T1336_i1, 3);
	Butterfly(T1336_i0, T1336_i1, &T1336_o0, &T1336_o1, T1336_W);
	PUT_FIFO(T1336_o0, 2);
	PUT_FIFO(T1336_o1, 3);

	GET_FIFO(T1337_i0, 1);
	GET_FIFO(T1337_i1, 3);
	Butterfly(T1337_i0, T1337_i1, &T1337_o0, &T1337_o1, T1337_W);
	PUT_FIFO(T1337_o0, 2);
	PUT_FIFO(T1337_o1, 3);

	GET_FIFO(T1338_i0, 1);
	GET_FIFO(T1338_i1, 3);
	Butterfly(T1338_i0, T1338_i1, &T1338_o0, &T1338_o1, T1338_W);
	PUT_FIFO(T1338_o0, 2);
	PUT_FIFO(T1338_o1, 3);

	GET_FIFO(T1339_i0, 1);
	GET_FIFO(T1339_i1, 3);
	Butterfly(T1339_i0, T1339_i1, &T1339_o0, &T1339_o1, T1339_W);
	PUT_FIFO(T1339_o0, 2);
	PUT_FIFO(T1339_o1, 3);

	GET_FIFO(T1340_i0, 1);
	GET_FIFO(T1340_i1, 3);
	Butterfly(T1340_i0, T1340_i1, &T1340_o0, &T1340_o1, T1340_W);
	PUT_FIFO(T1340_o0, 2);
	PUT_FIFO(T1340_o1, 3);

	GET_FIFO(T1341_i0, 1);
	GET_FIFO(T1341_i1, 3);
	Butterfly(T1341_i0, T1341_i1, &T1341_o0, &T1341_o1, T1341_W);
	PUT_FIFO(T1341_o0, 2);
	PUT_FIFO(T1341_o1, 3);

	GET_FIFO(T1342_i0, 1);
	GET_FIFO(T1342_i1, 3);
	Butterfly(T1342_i0, T1342_i1, &T1342_o0, &T1342_o1, T1342_W);
	PUT_FIFO(T1342_o0, 2);
	PUT_FIFO(T1342_o1, 3);

	GET_FIFO(T1343_i0, 1);
	GET_FIFO(T1343_i1, 3);
	Butterfly(T1343_i0, T1343_i1, &T1343_o0, &T1343_o1, T1343_W);
	PUT_FIFO(T1343_o0, 2);
	PUT_FIFO(T1343_o1, 3);

	GET_FIFO(T1344_i0, 0);
	GET_FIFO(T1344_i1, 2);
	Butterfly(T1344_i0, T1344_i1, &T1344_o0, &T1344_o1, T1344_W);
	PUT_FIFO(T1344_o0, 0);
	PUT_FIFO(T1344_o1, 1);

	GET_FIFO(T1345_i0, 0);
	GET_FIFO(T1345_i1, 2);
	Butterfly(T1345_i0, T1345_i1, &T1345_o0, &T1345_o1, T1345_W);
	PUT_FIFO(T1345_o0, 0);
	PUT_FIFO(T1345_o1, 1);

	GET_FIFO(T1346_i0, 0);
	GET_FIFO(T1346_i1, 2);
	Butterfly(T1346_i0, T1346_i1, &T1346_o0, &T1346_o1, T1346_W);
	PUT_FIFO(T1346_o0, 0);
	PUT_FIFO(T1346_o1, 1);

	GET_FIFO(T1347_i0, 0);
	GET_FIFO(T1347_i1, 2);
	Butterfly(T1347_i0, T1347_i1, &T1347_o0, &T1347_o1, T1347_W);
	PUT_FIFO(T1347_o0, 0);
	PUT_FIFO(T1347_o1, 1);

	GET_FIFO(T1348_i0, 0);
	GET_FIFO(T1348_i1, 2);
	Butterfly(T1348_i0, T1348_i1, &T1348_o0, &T1348_o1, T1348_W);
	PUT_FIFO(T1348_o0, 0);
	PUT_FIFO(T1348_o1, 1);

	GET_FIFO(T1349_i0, 0);
	GET_FIFO(T1349_i1, 2);
	Butterfly(T1349_i0, T1349_i1, &T1349_o0, &T1349_o1, T1349_W);
	PUT_FIFO(T1349_o0, 0);
	PUT_FIFO(T1349_o1, 1);

	GET_FIFO(T1350_i0, 0);
	GET_FIFO(T1350_i1, 2);
	Butterfly(T1350_i0, T1350_i1, &T1350_o0, &T1350_o1, T1350_W);
	PUT_FIFO(T1350_o0, 0);
	PUT_FIFO(T1350_o1, 1);

	GET_FIFO(T1351_i0, 0);
	GET_FIFO(T1351_i1, 2);
	Butterfly(T1351_i0, T1351_i1, &T1351_o0, &T1351_o1, T1351_W);
	PUT_FIFO(T1351_o0, 0);
	PUT_FIFO(T1351_o1, 1);

	GET_FIFO(T1352_i0, 0);
	GET_FIFO(T1352_i1, 2);
	Butterfly(T1352_i0, T1352_i1, &T1352_o0, &T1352_o1, T1352_W);
	PUT_FIFO(T1352_o0, 0);
	PUT_FIFO(T1352_o1, 1);

	GET_FIFO(T1353_i0, 0);
	GET_FIFO(T1353_i1, 2);
	Butterfly(T1353_i0, T1353_i1, &T1353_o0, &T1353_o1, T1353_W);
	PUT_FIFO(T1353_o0, 0);
	PUT_FIFO(T1353_o1, 1);

	GET_FIFO(T1354_i0, 0);
	GET_FIFO(T1354_i1, 2);
	Butterfly(T1354_i0, T1354_i1, &T1354_o0, &T1354_o1, T1354_W);
	PUT_FIFO(T1354_o0, 0);
	PUT_FIFO(T1354_o1, 1);

	GET_FIFO(T1355_i0, 0);
	GET_FIFO(T1355_i1, 2);
	Butterfly(T1355_i0, T1355_i1, &T1355_o0, &T1355_o1, T1355_W);
	PUT_FIFO(T1355_o0, 0);
	PUT_FIFO(T1355_o1, 1);

	GET_FIFO(T1356_i0, 0);
	GET_FIFO(T1356_i1, 2);
	Butterfly(T1356_i0, T1356_i1, &T1356_o0, &T1356_o1, T1356_W);
	PUT_FIFO(T1356_o0, 0);
	PUT_FIFO(T1356_o1, 1);

	GET_FIFO(T1357_i0, 0);
	GET_FIFO(T1357_i1, 2);
	Butterfly(T1357_i0, T1357_i1, &T1357_o0, &T1357_o1, T1357_W);
	PUT_FIFO(T1357_o0, 0);
	PUT_FIFO(T1357_o1, 1);

	GET_FIFO(T1358_i0, 0);
	GET_FIFO(T1358_i1, 2);
	Butterfly(T1358_i0, T1358_i1, &T1358_o0, &T1358_o1, T1358_W);
	PUT_FIFO(T1358_o0, 0);
	PUT_FIFO(T1358_o1, 1);

	GET_FIFO(T1359_i0, 0);
	GET_FIFO(T1359_i1, 2);
	Butterfly(T1359_i0, T1359_i1, &T1359_o0, &T1359_o1, T1359_W);
	PUT_FIFO(T1359_o0, 0);
	PUT_FIFO(T1359_o1, 1);

	GET_FIFO(T1360_i0, 1);
	GET_FIFO(T1360_i1, 3);
	Butterfly(T1360_i0, T1360_i1, &T1360_o0, &T1360_o1, T1360_W);
	PUT_FIFO(T1360_o0, 0);
	PUT_FIFO(T1360_o1, 1);

	GET_FIFO(T1361_i0, 1);
	GET_FIFO(T1361_i1, 3);
	Butterfly(T1361_i0, T1361_i1, &T1361_o0, &T1361_o1, T1361_W);
	PUT_FIFO(T1361_o0, 0);
	PUT_FIFO(T1361_o1, 1);

	GET_FIFO(T1362_i0, 1);
	GET_FIFO(T1362_i1, 3);
	Butterfly(T1362_i0, T1362_i1, &T1362_o0, &T1362_o1, T1362_W);
	PUT_FIFO(T1362_o0, 0);
	PUT_FIFO(T1362_o1, 1);

	GET_FIFO(T1363_i0, 1);
	GET_FIFO(T1363_i1, 3);
	Butterfly(T1363_i0, T1363_i1, &T1363_o0, &T1363_o1, T1363_W);
	PUT_FIFO(T1363_o0, 0);
	PUT_FIFO(T1363_o1, 1);

	GET_FIFO(T1364_i0, 1);
	GET_FIFO(T1364_i1, 3);
	Butterfly(T1364_i0, T1364_i1, &T1364_o0, &T1364_o1, T1364_W);
	PUT_FIFO(T1364_o0, 0);
	PUT_FIFO(T1364_o1, 1);

	GET_FIFO(T1365_i0, 1);
	GET_FIFO(T1365_i1, 3);
	Butterfly(T1365_i0, T1365_i1, &T1365_o0, &T1365_o1, T1365_W);
	PUT_FIFO(T1365_o0, 0);
	PUT_FIFO(T1365_o1, 1);

	GET_FIFO(T1366_i0, 1);
	GET_FIFO(T1366_i1, 3);
	Butterfly(T1366_i0, T1366_i1, &T1366_o0, &T1366_o1, T1366_W);
	PUT_FIFO(T1366_o0, 0);
	PUT_FIFO(T1366_o1, 1);

	GET_FIFO(T1367_i0, 1);
	GET_FIFO(T1367_i1, 3);
	Butterfly(T1367_i0, T1367_i1, &T1367_o0, &T1367_o1, T1367_W);
	PUT_FIFO(T1367_o0, 0);
	PUT_FIFO(T1367_o1, 1);

	GET_FIFO(T1368_i0, 1);
	GET_FIFO(T1368_i1, 3);
	Butterfly(T1368_i0, T1368_i1, &T1368_o0, &T1368_o1, T1368_W);
	PUT_FIFO(T1368_o0, 0);
	PUT_FIFO(T1368_o1, 1);

	GET_FIFO(T1369_i0, 1);
	GET_FIFO(T1369_i1, 3);
	Butterfly(T1369_i0, T1369_i1, &T1369_o0, &T1369_o1, T1369_W);
	PUT_FIFO(T1369_o0, 0);
	PUT_FIFO(T1369_o1, 1);

	GET_FIFO(T1370_i0, 1);
	GET_FIFO(T1370_i1, 3);
	Butterfly(T1370_i0, T1370_i1, &T1370_o0, &T1370_o1, T1370_W);
	PUT_FIFO(T1370_o0, 0);
	PUT_FIFO(T1370_o1, 1);

	GET_FIFO(T1371_i0, 1);
	GET_FIFO(T1371_i1, 3);
	Butterfly(T1371_i0, T1371_i1, &T1371_o0, &T1371_o1, T1371_W);
	PUT_FIFO(T1371_o0, 0);
	PUT_FIFO(T1371_o1, 1);

	GET_FIFO(T1372_i0, 1);
	GET_FIFO(T1372_i1, 3);
	Butterfly(T1372_i0, T1372_i1, &T1372_o0, &T1372_o1, T1372_W);
	PUT_FIFO(T1372_o0, 0);
	PUT_FIFO(T1372_o1, 1);

	GET_FIFO(T1373_i0, 1);
	GET_FIFO(T1373_i1, 3);
	Butterfly(T1373_i0, T1373_i1, &T1373_o0, &T1373_o1, T1373_W);
	PUT_FIFO(T1373_o0, 0);
	PUT_FIFO(T1373_o1, 1);

	GET_FIFO(T1374_i0, 1);
	GET_FIFO(T1374_i1, 3);
	Butterfly(T1374_i0, T1374_i1, &T1374_o0, &T1374_o1, T1374_W);
	PUT_FIFO(T1374_o0, 0);
	PUT_FIFO(T1374_o1, 1);

	GET_FIFO(T1375_i0, 1);
	GET_FIFO(T1375_i1, 3);
	Butterfly(T1375_i0, T1375_i1, &T1375_o0, &T1375_o1, T1375_W);
	PUT_FIFO(T1375_o0, 0);
	PUT_FIFO(T1375_o1, 1);

	GET_FIFO(T1376_i0, 0);
	GET_FIFO(T1376_i1, 2);
	Butterfly(T1376_i0, T1376_i1, &T1376_o0, &T1376_o1, T1376_W);
	PUT_FIFO(T1376_o0, 2);
	PUT_FIFO(T1376_o1, 3);

	GET_FIFO(T1377_i0, 0);
	GET_FIFO(T1377_i1, 2);
	Butterfly(T1377_i0, T1377_i1, &T1377_o0, &T1377_o1, T1377_W);
	PUT_FIFO(T1377_o0, 2);
	PUT_FIFO(T1377_o1, 3);

	GET_FIFO(T1378_i0, 0);
	GET_FIFO(T1378_i1, 2);
	Butterfly(T1378_i0, T1378_i1, &T1378_o0, &T1378_o1, T1378_W);
	PUT_FIFO(T1378_o0, 2);
	PUT_FIFO(T1378_o1, 3);

	GET_FIFO(T1379_i0, 0);
	GET_FIFO(T1379_i1, 2);
	Butterfly(T1379_i0, T1379_i1, &T1379_o0, &T1379_o1, T1379_W);
	PUT_FIFO(T1379_o0, 2);
	PUT_FIFO(T1379_o1, 3);

	GET_FIFO(T1380_i0, 0);
	GET_FIFO(T1380_i1, 2);
	Butterfly(T1380_i0, T1380_i1, &T1380_o0, &T1380_o1, T1380_W);
	PUT_FIFO(T1380_o0, 2);
	PUT_FIFO(T1380_o1, 3);

	GET_FIFO(T1381_i0, 0);
	GET_FIFO(T1381_i1, 2);
	Butterfly(T1381_i0, T1381_i1, &T1381_o0, &T1381_o1, T1381_W);
	PUT_FIFO(T1381_o0, 2);
	PUT_FIFO(T1381_o1, 3);

	GET_FIFO(T1382_i0, 0);
	GET_FIFO(T1382_i1, 2);
	Butterfly(T1382_i0, T1382_i1, &T1382_o0, &T1382_o1, T1382_W);
	PUT_FIFO(T1382_o0, 2);
	PUT_FIFO(T1382_o1, 3);

	GET_FIFO(T1383_i0, 0);
	GET_FIFO(T1383_i1, 2);
	Butterfly(T1383_i0, T1383_i1, &T1383_o0, &T1383_o1, T1383_W);
	PUT_FIFO(T1383_o0, 2);
	PUT_FIFO(T1383_o1, 3);

	GET_FIFO(T1384_i0, 0);
	GET_FIFO(T1384_i1, 2);
	Butterfly(T1384_i0, T1384_i1, &T1384_o0, &T1384_o1, T1384_W);
	PUT_FIFO(T1384_o0, 2);
	PUT_FIFO(T1384_o1, 3);

	GET_FIFO(T1385_i0, 0);
	GET_FIFO(T1385_i1, 2);
	Butterfly(T1385_i0, T1385_i1, &T1385_o0, &T1385_o1, T1385_W);
	PUT_FIFO(T1385_o0, 2);
	PUT_FIFO(T1385_o1, 3);

	GET_FIFO(T1386_i0, 0);
	GET_FIFO(T1386_i1, 2);
	Butterfly(T1386_i0, T1386_i1, &T1386_o0, &T1386_o1, T1386_W);
	PUT_FIFO(T1386_o0, 2);
	PUT_FIFO(T1386_o1, 3);

	GET_FIFO(T1387_i0, 0);
	GET_FIFO(T1387_i1, 2);
	Butterfly(T1387_i0, T1387_i1, &T1387_o0, &T1387_o1, T1387_W);
	PUT_FIFO(T1387_o0, 2);
	PUT_FIFO(T1387_o1, 3);

	GET_FIFO(T1388_i0, 0);
	GET_FIFO(T1388_i1, 2);
	Butterfly(T1388_i0, T1388_i1, &T1388_o0, &T1388_o1, T1388_W);
	PUT_FIFO(T1388_o0, 2);
	PUT_FIFO(T1388_o1, 3);

	GET_FIFO(T1389_i0, 0);
	GET_FIFO(T1389_i1, 2);
	Butterfly(T1389_i0, T1389_i1, &T1389_o0, &T1389_o1, T1389_W);
	PUT_FIFO(T1389_o0, 2);
	PUT_FIFO(T1389_o1, 3);

	GET_FIFO(T1390_i0, 0);
	GET_FIFO(T1390_i1, 2);
	Butterfly(T1390_i0, T1390_i1, &T1390_o0, &T1390_o1, T1390_W);
	PUT_FIFO(T1390_o0, 2);
	PUT_FIFO(T1390_o1, 3);

	GET_FIFO(T1391_i0, 0);
	GET_FIFO(T1391_i1, 2);
	Butterfly(T1391_i0, T1391_i1, &T1391_o0, &T1391_o1, T1391_W);
	PUT_FIFO(T1391_o0, 2);
	PUT_FIFO(T1391_o1, 3);

	GET_FIFO(T1392_i0, 1);
	GET_FIFO(T1392_i1, 3);
	Butterfly(T1392_i0, T1392_i1, &T1392_o0, &T1392_o1, T1392_W);
	PUT_FIFO(T1392_o0, 2);
	PUT_FIFO(T1392_o1, 3);

	GET_FIFO(T1393_i0, 1);
	GET_FIFO(T1393_i1, 3);
	Butterfly(T1393_i0, T1393_i1, &T1393_o0, &T1393_o1, T1393_W);
	PUT_FIFO(T1393_o0, 2);
	PUT_FIFO(T1393_o1, 3);

	GET_FIFO(T1394_i0, 1);
	GET_FIFO(T1394_i1, 3);
	Butterfly(T1394_i0, T1394_i1, &T1394_o0, &T1394_o1, T1394_W);
	PUT_FIFO(T1394_o0, 2);
	PUT_FIFO(T1394_o1, 3);

	GET_FIFO(T1395_i0, 1);
	GET_FIFO(T1395_i1, 3);
	Butterfly(T1395_i0, T1395_i1, &T1395_o0, &T1395_o1, T1395_W);
	PUT_FIFO(T1395_o0, 2);
	PUT_FIFO(T1395_o1, 3);

	GET_FIFO(T1396_i0, 1);
	GET_FIFO(T1396_i1, 3);
	Butterfly(T1396_i0, T1396_i1, &T1396_o0, &T1396_o1, T1396_W);
	PUT_FIFO(T1396_o0, 2);
	PUT_FIFO(T1396_o1, 3);

	GET_FIFO(T1397_i0, 1);
	GET_FIFO(T1397_i1, 3);
	Butterfly(T1397_i0, T1397_i1, &T1397_o0, &T1397_o1, T1397_W);
	PUT_FIFO(T1397_o0, 2);
	PUT_FIFO(T1397_o1, 3);

	GET_FIFO(T1398_i0, 1);
	GET_FIFO(T1398_i1, 3);
	Butterfly(T1398_i0, T1398_i1, &T1398_o0, &T1398_o1, T1398_W);
	PUT_FIFO(T1398_o0, 2);
	PUT_FIFO(T1398_o1, 3);

	GET_FIFO(T1399_i0, 1);
	GET_FIFO(T1399_i1, 3);
	Butterfly(T1399_i0, T1399_i1, &T1399_o0, &T1399_o1, T1399_W);
	PUT_FIFO(T1399_o0, 2);
	PUT_FIFO(T1399_o1, 3);

	GET_FIFO(T1400_i0, 1);
	GET_FIFO(T1400_i1, 3);
	Butterfly(T1400_i0, T1400_i1, &T1400_o0, &T1400_o1, T1400_W);
	PUT_FIFO(T1400_o0, 2);
	PUT_FIFO(T1400_o1, 3);

	GET_FIFO(T1401_i0, 1);
	GET_FIFO(T1401_i1, 3);
	Butterfly(T1401_i0, T1401_i1, &T1401_o0, &T1401_o1, T1401_W);
	PUT_FIFO(T1401_o0, 2);
	PUT_FIFO(T1401_o1, 3);

	GET_FIFO(T1402_i0, 1);
	GET_FIFO(T1402_i1, 3);
	Butterfly(T1402_i0, T1402_i1, &T1402_o0, &T1402_o1, T1402_W);
	PUT_FIFO(T1402_o0, 2);
	PUT_FIFO(T1402_o1, 3);

	GET_FIFO(T1403_i0, 1);
	GET_FIFO(T1403_i1, 3);
	Butterfly(T1403_i0, T1403_i1, &T1403_o0, &T1403_o1, T1403_W);
	PUT_FIFO(T1403_o0, 2);
	PUT_FIFO(T1403_o1, 3);

	GET_FIFO(T1404_i0, 1);
	GET_FIFO(T1404_i1, 3);
	Butterfly(T1404_i0, T1404_i1, &T1404_o0, &T1404_o1, T1404_W);
	PUT_FIFO(T1404_o0, 2);
	PUT_FIFO(T1404_o1, 3);

	GET_FIFO(T1405_i0, 1);
	GET_FIFO(T1405_i1, 3);
	Butterfly(T1405_i0, T1405_i1, &T1405_o0, &T1405_o1, T1405_W);
	PUT_FIFO(T1405_o0, 2);
	PUT_FIFO(T1405_o1, 3);

	GET_FIFO(T1406_i0, 1);
	GET_FIFO(T1406_i1, 3);
	Butterfly(T1406_i0, T1406_i1, &T1406_o0, &T1406_o1, T1406_W);
	PUT_FIFO(T1406_o0, 2);
	PUT_FIFO(T1406_o1, 3);

	GET_FIFO(T1407_i0, 1);
	GET_FIFO(T1407_i1, 3);
	Butterfly(T1407_i0, T1407_i1, &T1407_o0, &T1407_o1, T1407_W);
	PUT_FIFO(T1407_o0, 2);
	PUT_FIFO(T1407_o1, 3);

	GET_FIFO(T1408_i0, 0);
	GET_FIFO(T1408_i1, 2);
	Butterfly(T1408_i0, T1408_i1, &T1408_o0, &T1408_o1, T1408_W);
	PUT_FIFO(T1408_o0, 0);
	PUT_FIFO(T1408_o1, 1);

	GET_FIFO(T1409_i0, 0);
	GET_FIFO(T1409_i1, 2);
	Butterfly(T1409_i0, T1409_i1, &T1409_o0, &T1409_o1, T1409_W);
	PUT_FIFO(T1409_o0, 0);
	PUT_FIFO(T1409_o1, 1);

	GET_FIFO(T1410_i0, 0);
	GET_FIFO(T1410_i1, 2);
	Butterfly(T1410_i0, T1410_i1, &T1410_o0, &T1410_o1, T1410_W);
	PUT_FIFO(T1410_o0, 0);
	PUT_FIFO(T1410_o1, 1);

	GET_FIFO(T1411_i0, 0);
	GET_FIFO(T1411_i1, 2);
	Butterfly(T1411_i0, T1411_i1, &T1411_o0, &T1411_o1, T1411_W);
	PUT_FIFO(T1411_o0, 0);
	PUT_FIFO(T1411_o1, 1);

	GET_FIFO(T1412_i0, 0);
	GET_FIFO(T1412_i1, 2);
	Butterfly(T1412_i0, T1412_i1, &T1412_o0, &T1412_o1, T1412_W);
	PUT_FIFO(T1412_o0, 0);
	PUT_FIFO(T1412_o1, 1);

	GET_FIFO(T1413_i0, 0);
	GET_FIFO(T1413_i1, 2);
	Butterfly(T1413_i0, T1413_i1, &T1413_o0, &T1413_o1, T1413_W);
	PUT_FIFO(T1413_o0, 0);
	PUT_FIFO(T1413_o1, 1);

	GET_FIFO(T1414_i0, 0);
	GET_FIFO(T1414_i1, 2);
	Butterfly(T1414_i0, T1414_i1, &T1414_o0, &T1414_o1, T1414_W);
	PUT_FIFO(T1414_o0, 0);
	PUT_FIFO(T1414_o1, 1);

	GET_FIFO(T1415_i0, 0);
	GET_FIFO(T1415_i1, 2);
	Butterfly(T1415_i0, T1415_i1, &T1415_o0, &T1415_o1, T1415_W);
	PUT_FIFO(T1415_o0, 0);
	PUT_FIFO(T1415_o1, 1);

	GET_FIFO(T1416_i0, 0);
	GET_FIFO(T1416_i1, 2);
	Butterfly(T1416_i0, T1416_i1, &T1416_o0, &T1416_o1, T1416_W);
	PUT_FIFO(T1416_o0, 0);
	PUT_FIFO(T1416_o1, 1);

	GET_FIFO(T1417_i0, 0);
	GET_FIFO(T1417_i1, 2);
	Butterfly(T1417_i0, T1417_i1, &T1417_o0, &T1417_o1, T1417_W);
	PUT_FIFO(T1417_o0, 0);
	PUT_FIFO(T1417_o1, 1);

	GET_FIFO(T1418_i0, 0);
	GET_FIFO(T1418_i1, 2);
	Butterfly(T1418_i0, T1418_i1, &T1418_o0, &T1418_o1, T1418_W);
	PUT_FIFO(T1418_o0, 0);
	PUT_FIFO(T1418_o1, 1);

	GET_FIFO(T1419_i0, 0);
	GET_FIFO(T1419_i1, 2);
	Butterfly(T1419_i0, T1419_i1, &T1419_o0, &T1419_o1, T1419_W);
	PUT_FIFO(T1419_o0, 0);
	PUT_FIFO(T1419_o1, 1);

	GET_FIFO(T1420_i0, 0);
	GET_FIFO(T1420_i1, 2);
	Butterfly(T1420_i0, T1420_i1, &T1420_o0, &T1420_o1, T1420_W);
	PUT_FIFO(T1420_o0, 0);
	PUT_FIFO(T1420_o1, 1);

	GET_FIFO(T1421_i0, 0);
	GET_FIFO(T1421_i1, 2);
	Butterfly(T1421_i0, T1421_i1, &T1421_o0, &T1421_o1, T1421_W);
	PUT_FIFO(T1421_o0, 0);
	PUT_FIFO(T1421_o1, 1);

	GET_FIFO(T1422_i0, 0);
	GET_FIFO(T1422_i1, 2);
	Butterfly(T1422_i0, T1422_i1, &T1422_o0, &T1422_o1, T1422_W);
	PUT_FIFO(T1422_o0, 0);
	PUT_FIFO(T1422_o1, 1);

	GET_FIFO(T1423_i0, 0);
	GET_FIFO(T1423_i1, 2);
	Butterfly(T1423_i0, T1423_i1, &T1423_o0, &T1423_o1, T1423_W);
	PUT_FIFO(T1423_o0, 0);
	PUT_FIFO(T1423_o1, 1);

	GET_FIFO(T1424_i0, 1);
	GET_FIFO(T1424_i1, 3);
	Butterfly(T1424_i0, T1424_i1, &T1424_o0, &T1424_o1, T1424_W);
	PUT_FIFO(T1424_o0, 0);
	PUT_FIFO(T1424_o1, 1);

	GET_FIFO(T1425_i0, 1);
	GET_FIFO(T1425_i1, 3);
	Butterfly(T1425_i0, T1425_i1, &T1425_o0, &T1425_o1, T1425_W);
	PUT_FIFO(T1425_o0, 0);
	PUT_FIFO(T1425_o1, 1);

	GET_FIFO(T1426_i0, 1);
	GET_FIFO(T1426_i1, 3);
	Butterfly(T1426_i0, T1426_i1, &T1426_o0, &T1426_o1, T1426_W);
	PUT_FIFO(T1426_o0, 0);
	PUT_FIFO(T1426_o1, 1);

	GET_FIFO(T1427_i0, 1);
	GET_FIFO(T1427_i1, 3);
	Butterfly(T1427_i0, T1427_i1, &T1427_o0, &T1427_o1, T1427_W);
	PUT_FIFO(T1427_o0, 0);
	PUT_FIFO(T1427_o1, 1);

	GET_FIFO(T1428_i0, 1);
	GET_FIFO(T1428_i1, 3);
	Butterfly(T1428_i0, T1428_i1, &T1428_o0, &T1428_o1, T1428_W);
	PUT_FIFO(T1428_o0, 0);
	PUT_FIFO(T1428_o1, 1);

	GET_FIFO(T1429_i0, 1);
	GET_FIFO(T1429_i1, 3);
	Butterfly(T1429_i0, T1429_i1, &T1429_o0, &T1429_o1, T1429_W);
	PUT_FIFO(T1429_o0, 0);
	PUT_FIFO(T1429_o1, 1);

	GET_FIFO(T1430_i0, 1);
	GET_FIFO(T1430_i1, 3);
	Butterfly(T1430_i0, T1430_i1, &T1430_o0, &T1430_o1, T1430_W);
	PUT_FIFO(T1430_o0, 0);
	PUT_FIFO(T1430_o1, 1);

	GET_FIFO(T1431_i0, 1);
	GET_FIFO(T1431_i1, 3);
	Butterfly(T1431_i0, T1431_i1, &T1431_o0, &T1431_o1, T1431_W);
	PUT_FIFO(T1431_o0, 0);
	PUT_FIFO(T1431_o1, 1);

	GET_FIFO(T1432_i0, 1);
	GET_FIFO(T1432_i1, 3);
	Butterfly(T1432_i0, T1432_i1, &T1432_o0, &T1432_o1, T1432_W);
	PUT_FIFO(T1432_o0, 0);
	PUT_FIFO(T1432_o1, 1);

	GET_FIFO(T1433_i0, 1);
	GET_FIFO(T1433_i1, 3);
	Butterfly(T1433_i0, T1433_i1, &T1433_o0, &T1433_o1, T1433_W);
	PUT_FIFO(T1433_o0, 0);
	PUT_FIFO(T1433_o1, 1);

	GET_FIFO(T1434_i0, 1);
	GET_FIFO(T1434_i1, 3);
	Butterfly(T1434_i0, T1434_i1, &T1434_o0, &T1434_o1, T1434_W);
	PUT_FIFO(T1434_o0, 0);
	PUT_FIFO(T1434_o1, 1);

	GET_FIFO(T1435_i0, 1);
	GET_FIFO(T1435_i1, 3);
	Butterfly(T1435_i0, T1435_i1, &T1435_o0, &T1435_o1, T1435_W);
	PUT_FIFO(T1435_o0, 0);
	PUT_FIFO(T1435_o1, 1);

	GET_FIFO(T1436_i0, 1);
	GET_FIFO(T1436_i1, 3);
	Butterfly(T1436_i0, T1436_i1, &T1436_o0, &T1436_o1, T1436_W);
	PUT_FIFO(T1436_o0, 0);
	PUT_FIFO(T1436_o1, 1);

	GET_FIFO(T1437_i0, 1);
	GET_FIFO(T1437_i1, 3);
	Butterfly(T1437_i0, T1437_i1, &T1437_o0, &T1437_o1, T1437_W);
	PUT_FIFO(T1437_o0, 0);
	PUT_FIFO(T1437_o1, 1);

	GET_FIFO(T1438_i0, 1);
	GET_FIFO(T1438_i1, 3);
	Butterfly(T1438_i0, T1438_i1, &T1438_o0, &T1438_o1, T1438_W);
	PUT_FIFO(T1438_o0, 0);
	PUT_FIFO(T1438_o1, 1);

	GET_FIFO(T1439_i0, 1);
	GET_FIFO(T1439_i1, 3);
	Butterfly(T1439_i0, T1439_i1, &T1439_o0, &T1439_o1, T1439_W);
	PUT_FIFO(T1439_o0, 0);
	PUT_FIFO(T1439_o1, 1);

	GET_FIFO(T1440_i0, 0);
	GET_FIFO(T1440_i1, 2);
	Butterfly(T1440_i0, T1440_i1, &T1440_o0, &T1440_o1, T1440_W);
	PUT_FIFO(T1440_o0, 2);
	PUT_FIFO(T1440_o1, 3);

	GET_FIFO(T1441_i0, 0);
	GET_FIFO(T1441_i1, 2);
	Butterfly(T1441_i0, T1441_i1, &T1441_o0, &T1441_o1, T1441_W);
	PUT_FIFO(T1441_o0, 2);
	PUT_FIFO(T1441_o1, 3);

	GET_FIFO(T1442_i0, 0);
	GET_FIFO(T1442_i1, 2);
	Butterfly(T1442_i0, T1442_i1, &T1442_o0, &T1442_o1, T1442_W);
	PUT_FIFO(T1442_o0, 2);
	PUT_FIFO(T1442_o1, 3);

	GET_FIFO(T1443_i0, 0);
	GET_FIFO(T1443_i1, 2);
	Butterfly(T1443_i0, T1443_i1, &T1443_o0, &T1443_o1, T1443_W);
	PUT_FIFO(T1443_o0, 2);
	PUT_FIFO(T1443_o1, 3);

	GET_FIFO(T1444_i0, 0);
	GET_FIFO(T1444_i1, 2);
	Butterfly(T1444_i0, T1444_i1, &T1444_o0, &T1444_o1, T1444_W);
	PUT_FIFO(T1444_o0, 2);
	PUT_FIFO(T1444_o1, 3);

	GET_FIFO(T1445_i0, 0);
	GET_FIFO(T1445_i1, 2);
	Butterfly(T1445_i0, T1445_i1, &T1445_o0, &T1445_o1, T1445_W);
	PUT_FIFO(T1445_o0, 2);
	PUT_FIFO(T1445_o1, 3);

	GET_FIFO(T1446_i0, 0);
	GET_FIFO(T1446_i1, 2);
	Butterfly(T1446_i0, T1446_i1, &T1446_o0, &T1446_o1, T1446_W);
	PUT_FIFO(T1446_o0, 2);
	PUT_FIFO(T1446_o1, 3);

	GET_FIFO(T1447_i0, 0);
	GET_FIFO(T1447_i1, 2);
	Butterfly(T1447_i0, T1447_i1, &T1447_o0, &T1447_o1, T1447_W);
	PUT_FIFO(T1447_o0, 2);
	PUT_FIFO(T1447_o1, 3);

	GET_FIFO(T1448_i0, 0);
	GET_FIFO(T1448_i1, 2);
	Butterfly(T1448_i0, T1448_i1, &T1448_o0, &T1448_o1, T1448_W);
	PUT_FIFO(T1448_o0, 2);
	PUT_FIFO(T1448_o1, 3);

	GET_FIFO(T1449_i0, 0);
	GET_FIFO(T1449_i1, 2);
	Butterfly(T1449_i0, T1449_i1, &T1449_o0, &T1449_o1, T1449_W);
	PUT_FIFO(T1449_o0, 2);
	PUT_FIFO(T1449_o1, 3);

	GET_FIFO(T1450_i0, 0);
	GET_FIFO(T1450_i1, 2);
	Butterfly(T1450_i0, T1450_i1, &T1450_o0, &T1450_o1, T1450_W);
	PUT_FIFO(T1450_o0, 2);
	PUT_FIFO(T1450_o1, 3);

	GET_FIFO(T1451_i0, 0);
	GET_FIFO(T1451_i1, 2);
	Butterfly(T1451_i0, T1451_i1, &T1451_o0, &T1451_o1, T1451_W);
	PUT_FIFO(T1451_o0, 2);
	PUT_FIFO(T1451_o1, 3);

	GET_FIFO(T1452_i0, 0);
	GET_FIFO(T1452_i1, 2);
	Butterfly(T1452_i0, T1452_i1, &T1452_o0, &T1452_o1, T1452_W);
	PUT_FIFO(T1452_o0, 2);
	PUT_FIFO(T1452_o1, 3);

	GET_FIFO(T1453_i0, 0);
	GET_FIFO(T1453_i1, 2);
	Butterfly(T1453_i0, T1453_i1, &T1453_o0, &T1453_o1, T1453_W);
	PUT_FIFO(T1453_o0, 2);
	PUT_FIFO(T1453_o1, 3);

	GET_FIFO(T1454_i0, 0);
	GET_FIFO(T1454_i1, 2);
	Butterfly(T1454_i0, T1454_i1, &T1454_o0, &T1454_o1, T1454_W);
	PUT_FIFO(T1454_o0, 2);
	PUT_FIFO(T1454_o1, 3);

	GET_FIFO(T1455_i0, 0);
	GET_FIFO(T1455_i1, 2);
	Butterfly(T1455_i0, T1455_i1, &T1455_o0, &T1455_o1, T1455_W);
	PUT_FIFO(T1455_o0, 2);
	PUT_FIFO(T1455_o1, 3);

	GET_FIFO(T1456_i0, 1);
	GET_FIFO(T1456_i1, 3);
	Butterfly(T1456_i0, T1456_i1, &T1456_o0, &T1456_o1, T1456_W);
	PUT_FIFO(T1456_o0, 2);
	PUT_FIFO(T1456_o1, 3);

	GET_FIFO(T1457_i0, 1);
	GET_FIFO(T1457_i1, 3);
	Butterfly(T1457_i0, T1457_i1, &T1457_o0, &T1457_o1, T1457_W);
	PUT_FIFO(T1457_o0, 2);
	PUT_FIFO(T1457_o1, 3);

	GET_FIFO(T1458_i0, 1);
	GET_FIFO(T1458_i1, 3);
	Butterfly(T1458_i0, T1458_i1, &T1458_o0, &T1458_o1, T1458_W);
	PUT_FIFO(T1458_o0, 2);
	PUT_FIFO(T1458_o1, 3);

	GET_FIFO(T1459_i0, 1);
	GET_FIFO(T1459_i1, 3);
	Butterfly(T1459_i0, T1459_i1, &T1459_o0, &T1459_o1, T1459_W);
	PUT_FIFO(T1459_o0, 2);
	PUT_FIFO(T1459_o1, 3);

	GET_FIFO(T1460_i0, 1);
	GET_FIFO(T1460_i1, 3);
	Butterfly(T1460_i0, T1460_i1, &T1460_o0, &T1460_o1, T1460_W);
	PUT_FIFO(T1460_o0, 2);
	PUT_FIFO(T1460_o1, 3);

	GET_FIFO(T1461_i0, 1);
	GET_FIFO(T1461_i1, 3);
	Butterfly(T1461_i0, T1461_i1, &T1461_o0, &T1461_o1, T1461_W);
	PUT_FIFO(T1461_o0, 2);
	PUT_FIFO(T1461_o1, 3);

	GET_FIFO(T1462_i0, 1);
	GET_FIFO(T1462_i1, 3);
	Butterfly(T1462_i0, T1462_i1, &T1462_o0, &T1462_o1, T1462_W);
	PUT_FIFO(T1462_o0, 2);
	PUT_FIFO(T1462_o1, 3);

	GET_FIFO(T1463_i0, 1);
	GET_FIFO(T1463_i1, 3);
	Butterfly(T1463_i0, T1463_i1, &T1463_o0, &T1463_o1, T1463_W);
	PUT_FIFO(T1463_o0, 2);
	PUT_FIFO(T1463_o1, 3);

	GET_FIFO(T1464_i0, 1);
	GET_FIFO(T1464_i1, 3);
	Butterfly(T1464_i0, T1464_i1, &T1464_o0, &T1464_o1, T1464_W);
	PUT_FIFO(T1464_o0, 2);
	PUT_FIFO(T1464_o1, 3);

	GET_FIFO(T1465_i0, 1);
	GET_FIFO(T1465_i1, 3);
	Butterfly(T1465_i0, T1465_i1, &T1465_o0, &T1465_o1, T1465_W);
	PUT_FIFO(T1465_o0, 2);
	PUT_FIFO(T1465_o1, 3);

	GET_FIFO(T1466_i0, 1);
	GET_FIFO(T1466_i1, 3);
	Butterfly(T1466_i0, T1466_i1, &T1466_o0, &T1466_o1, T1466_W);
	PUT_FIFO(T1466_o0, 2);
	PUT_FIFO(T1466_o1, 3);

	GET_FIFO(T1467_i0, 1);
	GET_FIFO(T1467_i1, 3);
	Butterfly(T1467_i0, T1467_i1, &T1467_o0, &T1467_o1, T1467_W);
	PUT_FIFO(T1467_o0, 2);
	PUT_FIFO(T1467_o1, 3);

	GET_FIFO(T1468_i0, 1);
	GET_FIFO(T1468_i1, 3);
	Butterfly(T1468_i0, T1468_i1, &T1468_o0, &T1468_o1, T1468_W);
	PUT_FIFO(T1468_o0, 2);
	PUT_FIFO(T1468_o1, 3);

	GET_FIFO(T1469_i0, 1);
	GET_FIFO(T1469_i1, 3);
	Butterfly(T1469_i0, T1469_i1, &T1469_o0, &T1469_o1, T1469_W);
	PUT_FIFO(T1469_o0, 2);
	PUT_FIFO(T1469_o1, 3);

	GET_FIFO(T1470_i0, 1);
	GET_FIFO(T1470_i1, 3);
	Butterfly(T1470_i0, T1470_i1, &T1470_o0, &T1470_o1, T1470_W);
	PUT_FIFO(T1470_o0, 2);
	PUT_FIFO(T1470_o1, 3);

	GET_FIFO(T1471_i0, 1);
	GET_FIFO(T1471_i1, 3);
	Butterfly(T1471_i0, T1471_i1, &T1471_o0, &T1471_o1, T1471_W);
	PUT_FIFO(T1471_o0, 2);
	PUT_FIFO(T1471_o1, 3);

	GET_FIFO(T1472_i0, 0);
	GET_FIFO(T1472_i1, 2);
	Butterfly(T1472_i0, T1472_i1, &T1472_o0, &T1472_o1, T1472_W);
	PUT_FIFO(T1472_o0, 0);
	PUT_FIFO(T1472_o1, 1);

	GET_FIFO(T1473_i0, 0);
	GET_FIFO(T1473_i1, 2);
	Butterfly(T1473_i0, T1473_i1, &T1473_o0, &T1473_o1, T1473_W);
	PUT_FIFO(T1473_o0, 0);
	PUT_FIFO(T1473_o1, 1);

	GET_FIFO(T1474_i0, 0);
	GET_FIFO(T1474_i1, 2);
	Butterfly(T1474_i0, T1474_i1, &T1474_o0, &T1474_o1, T1474_W);
	PUT_FIFO(T1474_o0, 0);
	PUT_FIFO(T1474_o1, 1);

	GET_FIFO(T1475_i0, 0);
	GET_FIFO(T1475_i1, 2);
	Butterfly(T1475_i0, T1475_i1, &T1475_o0, &T1475_o1, T1475_W);
	PUT_FIFO(T1475_o0, 0);
	PUT_FIFO(T1475_o1, 1);

	GET_FIFO(T1476_i0, 0);
	GET_FIFO(T1476_i1, 2);
	Butterfly(T1476_i0, T1476_i1, &T1476_o0, &T1476_o1, T1476_W);
	PUT_FIFO(T1476_o0, 0);
	PUT_FIFO(T1476_o1, 1);

	GET_FIFO(T1477_i0, 0);
	GET_FIFO(T1477_i1, 2);
	Butterfly(T1477_i0, T1477_i1, &T1477_o0, &T1477_o1, T1477_W);
	PUT_FIFO(T1477_o0, 0);
	PUT_FIFO(T1477_o1, 1);

	GET_FIFO(T1478_i0, 0);
	GET_FIFO(T1478_i1, 2);
	Butterfly(T1478_i0, T1478_i1, &T1478_o0, &T1478_o1, T1478_W);
	PUT_FIFO(T1478_o0, 0);
	PUT_FIFO(T1478_o1, 1);

	GET_FIFO(T1479_i0, 0);
	GET_FIFO(T1479_i1, 2);
	Butterfly(T1479_i0, T1479_i1, &T1479_o0, &T1479_o1, T1479_W);
	PUT_FIFO(T1479_o0, 0);
	PUT_FIFO(T1479_o1, 1);

	GET_FIFO(T1480_i0, 0);
	GET_FIFO(T1480_i1, 2);
	Butterfly(T1480_i0, T1480_i1, &T1480_o0, &T1480_o1, T1480_W);
	PUT_FIFO(T1480_o0, 0);
	PUT_FIFO(T1480_o1, 1);

	GET_FIFO(T1481_i0, 0);
	GET_FIFO(T1481_i1, 2);
	Butterfly(T1481_i0, T1481_i1, &T1481_o0, &T1481_o1, T1481_W);
	PUT_FIFO(T1481_o0, 0);
	PUT_FIFO(T1481_o1, 1);

	GET_FIFO(T1482_i0, 0);
	GET_FIFO(T1482_i1, 2);
	Butterfly(T1482_i0, T1482_i1, &T1482_o0, &T1482_o1, T1482_W);
	PUT_FIFO(T1482_o0, 0);
	PUT_FIFO(T1482_o1, 1);

	GET_FIFO(T1483_i0, 0);
	GET_FIFO(T1483_i1, 2);
	Butterfly(T1483_i0, T1483_i1, &T1483_o0, &T1483_o1, T1483_W);
	PUT_FIFO(T1483_o0, 0);
	PUT_FIFO(T1483_o1, 1);

	GET_FIFO(T1484_i0, 0);
	GET_FIFO(T1484_i1, 2);
	Butterfly(T1484_i0, T1484_i1, &T1484_o0, &T1484_o1, T1484_W);
	PUT_FIFO(T1484_o0, 0);
	PUT_FIFO(T1484_o1, 1);

	GET_FIFO(T1485_i0, 0);
	GET_FIFO(T1485_i1, 2);
	Butterfly(T1485_i0, T1485_i1, &T1485_o0, &T1485_o1, T1485_W);
	PUT_FIFO(T1485_o0, 0);
	PUT_FIFO(T1485_o1, 1);

	GET_FIFO(T1486_i0, 0);
	GET_FIFO(T1486_i1, 2);
	Butterfly(T1486_i0, T1486_i1, &T1486_o0, &T1486_o1, T1486_W);
	PUT_FIFO(T1486_o0, 0);
	PUT_FIFO(T1486_o1, 1);

	GET_FIFO(T1487_i0, 0);
	GET_FIFO(T1487_i1, 2);
	Butterfly(T1487_i0, T1487_i1, &T1487_o0, &T1487_o1, T1487_W);
	PUT_FIFO(T1487_o0, 0);
	PUT_FIFO(T1487_o1, 1);

	GET_FIFO(T1488_i0, 1);
	GET_FIFO(T1488_i1, 3);
	Butterfly(T1488_i0, T1488_i1, &T1488_o0, &T1488_o1, T1488_W);
	PUT_FIFO(T1488_o0, 0);
	PUT_FIFO(T1488_o1, 1);

	GET_FIFO(T1489_i0, 1);
	GET_FIFO(T1489_i1, 3);
	Butterfly(T1489_i0, T1489_i1, &T1489_o0, &T1489_o1, T1489_W);
	PUT_FIFO(T1489_o0, 0);
	PUT_FIFO(T1489_o1, 1);

	GET_FIFO(T1490_i0, 1);
	GET_FIFO(T1490_i1, 3);
	Butterfly(T1490_i0, T1490_i1, &T1490_o0, &T1490_o1, T1490_W);
	PUT_FIFO(T1490_o0, 0);
	PUT_FIFO(T1490_o1, 1);

	GET_FIFO(T1491_i0, 1);
	GET_FIFO(T1491_i1, 3);
	Butterfly(T1491_i0, T1491_i1, &T1491_o0, &T1491_o1, T1491_W);
	PUT_FIFO(T1491_o0, 0);
	PUT_FIFO(T1491_o1, 1);

	GET_FIFO(T1492_i0, 1);
	GET_FIFO(T1492_i1, 3);
	Butterfly(T1492_i0, T1492_i1, &T1492_o0, &T1492_o1, T1492_W);
	PUT_FIFO(T1492_o0, 0);
	PUT_FIFO(T1492_o1, 1);

	GET_FIFO(T1493_i0, 1);
	GET_FIFO(T1493_i1, 3);
	Butterfly(T1493_i0, T1493_i1, &T1493_o0, &T1493_o1, T1493_W);
	PUT_FIFO(T1493_o0, 0);
	PUT_FIFO(T1493_o1, 1);

	GET_FIFO(T1494_i0, 1);
	GET_FIFO(T1494_i1, 3);
	Butterfly(T1494_i0, T1494_i1, &T1494_o0, &T1494_o1, T1494_W);
	PUT_FIFO(T1494_o0, 0);
	PUT_FIFO(T1494_o1, 1);

	GET_FIFO(T1495_i0, 1);
	GET_FIFO(T1495_i1, 3);
	Butterfly(T1495_i0, T1495_i1, &T1495_o0, &T1495_o1, T1495_W);
	PUT_FIFO(T1495_o0, 0);
	PUT_FIFO(T1495_o1, 1);

	GET_FIFO(T1496_i0, 1);
	GET_FIFO(T1496_i1, 3);
	Butterfly(T1496_i0, T1496_i1, &T1496_o0, &T1496_o1, T1496_W);
	PUT_FIFO(T1496_o0, 0);
	PUT_FIFO(T1496_o1, 1);

	GET_FIFO(T1497_i0, 1);
	GET_FIFO(T1497_i1, 3);
	Butterfly(T1497_i0, T1497_i1, &T1497_o0, &T1497_o1, T1497_W);
	PUT_FIFO(T1497_o0, 0);
	PUT_FIFO(T1497_o1, 1);

	GET_FIFO(T1498_i0, 1);
	GET_FIFO(T1498_i1, 3);
	Butterfly(T1498_i0, T1498_i1, &T1498_o0, &T1498_o1, T1498_W);
	PUT_FIFO(T1498_o0, 0);
	PUT_FIFO(T1498_o1, 1);

	GET_FIFO(T1499_i0, 1);
	GET_FIFO(T1499_i1, 3);
	Butterfly(T1499_i0, T1499_i1, &T1499_o0, &T1499_o1, T1499_W);
	PUT_FIFO(T1499_o0, 0);
	PUT_FIFO(T1499_o1, 1);

	GET_FIFO(T1500_i0, 1);
	GET_FIFO(T1500_i1, 3);
	Butterfly(T1500_i0, T1500_i1, &T1500_o0, &T1500_o1, T1500_W);
	PUT_FIFO(T1500_o0, 0);
	PUT_FIFO(T1500_o1, 1);

	GET_FIFO(T1501_i0, 1);
	GET_FIFO(T1501_i1, 3);
	Butterfly(T1501_i0, T1501_i1, &T1501_o0, &T1501_o1, T1501_W);
	PUT_FIFO(T1501_o0, 0);
	PUT_FIFO(T1501_o1, 1);

	GET_FIFO(T1502_i0, 1);
	GET_FIFO(T1502_i1, 3);
	Butterfly(T1502_i0, T1502_i1, &T1502_o0, &T1502_o1, T1502_W);
	PUT_FIFO(T1502_o0, 0);
	PUT_FIFO(T1502_o1, 1);

	GET_FIFO(T1503_i0, 1);
	GET_FIFO(T1503_i1, 3);
	Butterfly(T1503_i0, T1503_i1, &T1503_o0, &T1503_o1, T1503_W);
	PUT_FIFO(T1503_o0, 0);
	PUT_FIFO(T1503_o1, 1);

	GET_FIFO(T1504_i0, 0);
	GET_FIFO(T1504_i1, 2);
	Butterfly(T1504_i0, T1504_i1, &T1504_o0, &T1504_o1, T1504_W);
	PUT_FIFO(T1504_o0, 2);
	PUT_FIFO(T1504_o1, 3);

	GET_FIFO(T1505_i0, 0);
	GET_FIFO(T1505_i1, 2);
	Butterfly(T1505_i0, T1505_i1, &T1505_o0, &T1505_o1, T1505_W);
	PUT_FIFO(T1505_o0, 2);
	PUT_FIFO(T1505_o1, 3);

	GET_FIFO(T1506_i0, 0);
	GET_FIFO(T1506_i1, 2);
	Butterfly(T1506_i0, T1506_i1, &T1506_o0, &T1506_o1, T1506_W);
	PUT_FIFO(T1506_o0, 2);
	PUT_FIFO(T1506_o1, 3);

	GET_FIFO(T1507_i0, 0);
	GET_FIFO(T1507_i1, 2);
	Butterfly(T1507_i0, T1507_i1, &T1507_o0, &T1507_o1, T1507_W);
	PUT_FIFO(T1507_o0, 2);
	PUT_FIFO(T1507_o1, 3);

	GET_FIFO(T1508_i0, 0);
	GET_FIFO(T1508_i1, 2);
	Butterfly(T1508_i0, T1508_i1, &T1508_o0, &T1508_o1, T1508_W);
	PUT_FIFO(T1508_o0, 2);
	PUT_FIFO(T1508_o1, 3);

	GET_FIFO(T1509_i0, 0);
	GET_FIFO(T1509_i1, 2);
	Butterfly(T1509_i0, T1509_i1, &T1509_o0, &T1509_o1, T1509_W);
	PUT_FIFO(T1509_o0, 2);
	PUT_FIFO(T1509_o1, 3);

	GET_FIFO(T1510_i0, 0);
	GET_FIFO(T1510_i1, 2);
	Butterfly(T1510_i0, T1510_i1, &T1510_o0, &T1510_o1, T1510_W);
	PUT_FIFO(T1510_o0, 2);
	PUT_FIFO(T1510_o1, 3);

	GET_FIFO(T1511_i0, 0);
	GET_FIFO(T1511_i1, 2);
	Butterfly(T1511_i0, T1511_i1, &T1511_o0, &T1511_o1, T1511_W);
	PUT_FIFO(T1511_o0, 2);
	PUT_FIFO(T1511_o1, 3);

	GET_FIFO(T1512_i0, 0);
	GET_FIFO(T1512_i1, 2);
	Butterfly(T1512_i0, T1512_i1, &T1512_o0, &T1512_o1, T1512_W);
	PUT_FIFO(T1512_o0, 2);
	PUT_FIFO(T1512_o1, 3);

	GET_FIFO(T1513_i0, 0);
	GET_FIFO(T1513_i1, 2);
	Butterfly(T1513_i0, T1513_i1, &T1513_o0, &T1513_o1, T1513_W);
	PUT_FIFO(T1513_o0, 2);
	PUT_FIFO(T1513_o1, 3);

	GET_FIFO(T1514_i0, 0);
	GET_FIFO(T1514_i1, 2);
	Butterfly(T1514_i0, T1514_i1, &T1514_o0, &T1514_o1, T1514_W);
	PUT_FIFO(T1514_o0, 2);
	PUT_FIFO(T1514_o1, 3);

	GET_FIFO(T1515_i0, 0);
	GET_FIFO(T1515_i1, 2);
	Butterfly(T1515_i0, T1515_i1, &T1515_o0, &T1515_o1, T1515_W);
	PUT_FIFO(T1515_o0, 2);
	PUT_FIFO(T1515_o1, 3);

	GET_FIFO(T1516_i0, 0);
	GET_FIFO(T1516_i1, 2);
	Butterfly(T1516_i0, T1516_i1, &T1516_o0, &T1516_o1, T1516_W);
	PUT_FIFO(T1516_o0, 2);
	PUT_FIFO(T1516_o1, 3);

	GET_FIFO(T1517_i0, 0);
	GET_FIFO(T1517_i1, 2);
	Butterfly(T1517_i0, T1517_i1, &T1517_o0, &T1517_o1, T1517_W);
	PUT_FIFO(T1517_o0, 2);
	PUT_FIFO(T1517_o1, 3);

	GET_FIFO(T1518_i0, 0);
	GET_FIFO(T1518_i1, 2);
	Butterfly(T1518_i0, T1518_i1, &T1518_o0, &T1518_o1, T1518_W);
	PUT_FIFO(T1518_o0, 2);
	PUT_FIFO(T1518_o1, 3);

	GET_FIFO(T1519_i0, 0);
	GET_FIFO(T1519_i1, 2);
	Butterfly(T1519_i0, T1519_i1, &T1519_o0, &T1519_o1, T1519_W);
	PUT_FIFO(T1519_o0, 2);
	PUT_FIFO(T1519_o1, 3);

	GET_FIFO(T1520_i0, 1);
	GET_FIFO(T1520_i1, 3);
	Butterfly(T1520_i0, T1520_i1, &T1520_o0, &T1520_o1, T1520_W);
	PUT_FIFO(T1520_o0, 2);
	PUT_FIFO(T1520_o1, 3);

	GET_FIFO(T1521_i0, 1);
	GET_FIFO(T1521_i1, 3);
	Butterfly(T1521_i0, T1521_i1, &T1521_o0, &T1521_o1, T1521_W);
	PUT_FIFO(T1521_o0, 2);
	PUT_FIFO(T1521_o1, 3);

	GET_FIFO(T1522_i0, 1);
	GET_FIFO(T1522_i1, 3);
	Butterfly(T1522_i0, T1522_i1, &T1522_o0, &T1522_o1, T1522_W);
	PUT_FIFO(T1522_o0, 2);
	PUT_FIFO(T1522_o1, 3);

	GET_FIFO(T1523_i0, 1);
	GET_FIFO(T1523_i1, 3);
	Butterfly(T1523_i0, T1523_i1, &T1523_o0, &T1523_o1, T1523_W);
	PUT_FIFO(T1523_o0, 2);
	PUT_FIFO(T1523_o1, 3);

	GET_FIFO(T1524_i0, 1);
	GET_FIFO(T1524_i1, 3);
	Butterfly(T1524_i0, T1524_i1, &T1524_o0, &T1524_o1, T1524_W);
	PUT_FIFO(T1524_o0, 2);
	PUT_FIFO(T1524_o1, 3);

	GET_FIFO(T1525_i0, 1);
	GET_FIFO(T1525_i1, 3);
	Butterfly(T1525_i0, T1525_i1, &T1525_o0, &T1525_o1, T1525_W);
	PUT_FIFO(T1525_o0, 2);
	PUT_FIFO(T1525_o1, 3);

	GET_FIFO(T1526_i0, 1);
	GET_FIFO(T1526_i1, 3);
	Butterfly(T1526_i0, T1526_i1, &T1526_o0, &T1526_o1, T1526_W);
	PUT_FIFO(T1526_o0, 2);
	PUT_FIFO(T1526_o1, 3);

	GET_FIFO(T1527_i0, 1);
	GET_FIFO(T1527_i1, 3);
	Butterfly(T1527_i0, T1527_i1, &T1527_o0, &T1527_o1, T1527_W);
	PUT_FIFO(T1527_o0, 2);
	PUT_FIFO(T1527_o1, 3);

	GET_FIFO(T1528_i0, 1);
	GET_FIFO(T1528_i1, 3);
	Butterfly(T1528_i0, T1528_i1, &T1528_o0, &T1528_o1, T1528_W);
	PUT_FIFO(T1528_o0, 2);
	PUT_FIFO(T1528_o1, 3);

	GET_FIFO(T1529_i0, 1);
	GET_FIFO(T1529_i1, 3);
	Butterfly(T1529_i0, T1529_i1, &T1529_o0, &T1529_o1, T1529_W);
	PUT_FIFO(T1529_o0, 2);
	PUT_FIFO(T1529_o1, 3);

	GET_FIFO(T1530_i0, 1);
	GET_FIFO(T1530_i1, 3);
	Butterfly(T1530_i0, T1530_i1, &T1530_o0, &T1530_o1, T1530_W);
	PUT_FIFO(T1530_o0, 2);
	PUT_FIFO(T1530_o1, 3);

	GET_FIFO(T1531_i0, 1);
	GET_FIFO(T1531_i1, 3);
	Butterfly(T1531_i0, T1531_i1, &T1531_o0, &T1531_o1, T1531_W);
	PUT_FIFO(T1531_o0, 2);
	PUT_FIFO(T1531_o1, 3);

	GET_FIFO(T1532_i0, 1);
	GET_FIFO(T1532_i1, 3);
	Butterfly(T1532_i0, T1532_i1, &T1532_o0, &T1532_o1, T1532_W);
	PUT_FIFO(T1532_o0, 2);
	PUT_FIFO(T1532_o1, 3);

	GET_FIFO(T1533_i0, 1);
	GET_FIFO(T1533_i1, 3);
	Butterfly(T1533_i0, T1533_i1, &T1533_o0, &T1533_o1, T1533_W);
	PUT_FIFO(T1533_o0, 2);
	PUT_FIFO(T1533_o1, 3);

	GET_FIFO(T1534_i0, 1);
	GET_FIFO(T1534_i1, 3);
	Butterfly(T1534_i0, T1534_i1, &T1534_o0, &T1534_o1, T1534_W);
	PUT_FIFO(T1534_o0, 2);
	PUT_FIFO(T1534_o1, 3);

	GET_FIFO(T1535_i0, 1);
	GET_FIFO(T1535_i1, 3);
	Butterfly(T1535_i0, T1535_i1, &T1535_o0, &T1535_o1, T1535_W);
	PUT_FIFO(T1535_o0, 2);
	PUT_FIFO(T1535_o1, 3);
}

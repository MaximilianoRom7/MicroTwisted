while $(true)
do
    start=`date +%s`;
    # --------------------------------------------------------
    curl http://0.0.0.0:5000/service1/route1 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service1/route2 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service1/route3 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service2/route1 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service2/route2 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service2/route3 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service3/route1 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service3/route2 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service3/route3 2&>1 > /dev/null;
    # --------------------------------------------------------
    curl http://0.0.0.0:5000/service1/route1 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service1/route2 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service1/route3 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service2/route1 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service2/route2 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service2/route3 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service3/route1 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service3/route2 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service3/route3 2&>1 > /dev/null;
    # --------------------------------------------------------
    curl http://0.0.0.0:5000/service1/route1 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service1/route2 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service1/route3 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service2/route1 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service2/route2 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service2/route3 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service3/route1 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service3/route2 2&>1 > /dev/null;
    curl http://0.0.0.0:5000/service3/route3 2&>1 > /dev/null;
    end=`date +%s`;
    runtime=$((end-start));
    echo "ELAPSE: "$runtime;
done

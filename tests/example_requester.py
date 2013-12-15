#!/usr/bin/env python

""" Requester usage example. """

import rospy
from scheduler_msgs.msg import Request
from scheduler_msgs.msg import Resource
from rocon_scheduler_requests import TransitionError
from rocon_scheduler_requests.requester import Requester


def feedback(rset):
    """ Scheduler feedback function. """
    for rq in rset.values():
        if rq.msg.status == Request.WAITING:
            rospy.loginfo('Request queued: ' + str(rq.get_uuid()))
        elif rq.msg.status == Request.GRANTED:
            rospy.loginfo('Request granted: ' + str(rq.get_uuid()))
        elif rq.msg.status == Request.RELEASED:
            rospy.loginfo('Request canceled: ' + str(rq.get_uuid()))

if __name__ == '__main__':
    rospy.init_node("example_requester")
    rqr = Requester(feedback)

    rospy.loginfo('requesting any tutlebot able to run example_rapp')
    resource = Resource(name='example_rapp',
                        platform_info='linux.*.ros.turtlebot.*')
    request_id = rqr.new_request([resource])
    rqr.send_requests()

    # Loop once every two seconds in the main thread.
    cycle = rospy.Rate(0.5)
    while not rospy.is_shutdown():
        cycle.sleep()
        try:
            # cancel the previously-issued request
            rqr.rset[request_id].cancel()
        except KeyError:
            rospy.loginfo('old request no longer exists: '
                          + str(request_id))
            rospy.loginfo('requesting another similar robot now')
            request_id = rqr.new_request([resource])
            rqr.send_requests()
        except TransitionError:
            rospy.loginfo('request not releasable: ' + str(request_id))
            rqr.cancel_all()
            rqr.send_requests()

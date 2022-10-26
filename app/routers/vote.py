from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models
from ..schemas import vote_schema
from ..database import get_db
from .. import oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Voting"]
)


@router.post("/")
def vote_on_post(
        vote: vote_schema.VoteBase,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(oauth2.get_current_user)
):
    """A user can add or remove vote on any published post"""

    # check that post exists and is in published state
    post = db.query(models.Post).filter(models.Post.id == vote.post_id, models.Post.is_published == True).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no published post with given id")

    # vote
    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id,
        models.Vote.post_id == vote.post_id)

    voted_already = vote_query.first()

    if not voted_already:
        if vote.vote == 1:
            add_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
            db.add(add_vote)
            db.commit()
            return {"message": "Successfully added your vote!"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Failed to remove your vote: you haven't voted fot this post yet.")
    elif voted_already:
        if vote.vote == 0:
            vote_query.delete()
            db.commit()
            return {"message": "Successfully removed your vote!"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Failed to add vote: you have already voted for this post.")
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Unable to vote.")
